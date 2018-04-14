#!/usr/bin/perl
package similarity;

use strict;
use Encode;
use utf8;

use File::Basename;

use KyotoCabinet;
my $tfidf_db   = new KyotoCabinet::DB;
my $tfidf_file = 'tfidf.kch';
my $title_db = new KyotoCabinet::DB;
my $title_file = 'title.kch';
my $index_db = new KyotoCabinet::DB;
my $index_file = 'index.kch';

my $N = 188627;

sub get {
    my ($query) = @_;
    my $object_file = decode_utf8($query);
    my %object_vector = create_vector($object_file);
    my @search_result = search_article(\%object_vector);

    my %score_hash;
    foreach my $file (sort @search_result) {
        my %result_vector = create_vector($file);
        my $cos = calc_cosin(\%object_vector,\%result_vector);
        if($cos > 0.3) {
            $score_hash{$file} = $cos;
        }
    }
    undef @search_result;

    return %score_hash;
}

sub calc_cosin {
    my ($obj_vec, $res_vec) = @_;
    my ($vo, $vr, $vor) = (0, 0, 0);

    foreach my $obj_key (keys %{$obj_vec}) {
        $vo += $$obj_vec{$obj_key} ** 2;
        foreach my $res_key (keys %{$res_vec}) {
            if ($obj_key eq $res_key) {
                $vor += $$obj_vec{$obj_key} * $$res_vec{$res_key};
            }
        }
    }

    foreach my $res_key (keys %{$res_vec}) {
        $vr += $$res_vec{$res_key} ** 2;
    }

    my ($norm_o, $norm_r) = (sqrt($vo), sqrt($vr));
    if ($norm_o * $norm_r == 0) {
        return 0;
    } else {
        return $vor / ($norm_o * $norm_r);
    }
}

sub search_article {
    my %articles;

    $index_db->open($index_file, $index_db->OREADER);
    foreach my $key (keys %{$_[0]}) {
        my $index = $index_db->get($key);
        foreach my $file (split(',', $index)) {
            ($file) = split(':', $file);
            $articles{$file}++;
        }
    }
    $index_db->close();

    return keys %articles;
}

sub create_vector {
    my $id = basename($_[0]);

    $tfidf_db->open($tfidf_file, $tfidf_db->OREADER);
    my @tfidf_list = split(',', $tfidf_db->get($id));
    $tfidf_db->close();

    my %vector;
    foreach my $index (@tfidf_list) {
        my ($word, $tfidf) = split(':', $index);
        $vector{$word} = $tfidf;
    }
    return %vector;
}


