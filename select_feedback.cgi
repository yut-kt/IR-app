#!/usr/bin/perl 
require 'CommonHtml.cgi';
require 'Common.cgi';

use strict;
use Encode;
use utf8;

use CGI;
my $q = new CGI;

use KyotoCabinet;

my $index_db = new KyotoCabinet::DB;
my $index_file = "index.kch";

my $title_db = new KyotoCabinet::DB;
my $title_file = "title.kch";

my $tfidf_db = new KyotoCabinet::DB;
my $tfidf_file = "tfidf.kch";

use File::Basename;

my $N = 188627;

main();

sub main
{
    print_html::header();

    my %count;

    # open DB
    $index_db->open($index_file, $index_db->OREADER);
    $title_db->open($title_file, $title_db->OREADER);
    $tfidf_db->open($tfidf_file, $tfidf_db->OREADER);

    my @feedback_files = $q->param('check');
    my %tfidf;
    foreach my $file (@feedback_files) {
        my %obj_vector = create_vector($file);
        foreach my $key (keys %obj_vector) {
            $tfidf{$key} += $obj_vector{$key};
        }
    }

    my @search_result = search_article(\%tfidf);
    my %score_hash;
    foreach my $file (sort @search_result) {
        my %obj_vector = create_vector($file);
        my $cos = calc_cosin(\%tfidf, \%obj_vector);
        if ($cos > 0.3) {
            $score_hash{$file} = $cos;
        }
    }
    undef @search_result;

    # sort hash
    my @sorted_file_list = hash_value::sort(\%score_hash);


    my $query = decode_utf8($q->param('query'));

    my $rank = 1;
    print "<form method=post type=checkbox action='select_feedback.cgi?0'>\n";
    print "<input type=hidden name='query' value=$query>";
    print "<input type=submit value='フィードバック'><br><br>\n";
    print "<ul>\n";
    foreach my $key (@sorted_file_list) {
        my $url = "view_original.cgi?$key+$query";
        my $title = decode_utf8($title_db->get(basename($key)));
        print encode_utf8("<li><input type=checkbox name=check value=$key>\n");
        print encode_utf8("<a href=$url>$rank --> $title</a></li><br>\n");
        $rank++;
    }
    print "</ul>\n";
    print "</form>\n";
    print_html::fotter();

    undef @sorted_file_list;
    undef %tfidf;

    $index_db->close();
}


sub calc_cosin
{
    my ($object_vector, $result_vector) = @_;
    my $vo = 0;
    my $vr = 0;
    my $vor = 0;

    foreach my $object_key (keys %{$object_vector})
    {
        $vo += $$object_vector{$object_key} ** 2;
        foreach my $result_key (keys %{$result_vector})
        {
            if ($object_key eq $result_key)
            {
                $vor += $$object_vector{$object_key} * $$result_vector{$result_key};
            }
        }
    }

    foreach my $result_key (keys %{$result_vector})
    {
        $vr += $$result_vector{$result_key} ** 2;
    }

    my $norm_o = sqrt($vo);
    my $norm_r = sqrt($vr);

    if ($norm_o * $norm_r == 0)
    {
        return 0;
    }
    else
    {
        return $vor / ($norm_o * $norm_r);
    }
}

sub search_article
{
    my $index_db = new KyotoCabinet::DB;
    my $index_file = 'index.kch';

    $index_db->open($index_file, $index_db->OREADER);

    my ($hash) = @_;

    my %result;

    my @articles;
    foreach my $key (keys %{$hash})
    {
        my $index = $index_db->get($key);
        my @files = split(',', $index);

        foreach my $file(@files)
        {
            ($file) = split(':', $file);
            $result{$file}++;
        }
    }
    $index_db->close();

    foreach my $key (keys %result)
    {
        push(@articles, $key);
    }

    return @articles;
}

sub create_vector
{
    my ($url) = @_;
    my $file = basename($url);

    $tfidf_db->open($tfidf_file, $tfidf_db->OREADER);

    my @tfidf_list = split(',', $tfidf_db->get($file));

    my %hash;

    foreach my $index (@tfidf_list)
    {
        my ($word, $tfidf) = split(':', $index);
        $hash{$word} = $tfidf;
    }
    $tfidf_db->close();
    return %hash;
}
