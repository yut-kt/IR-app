#!/usr/bin/perl
require 'CommonHtml.cgi';
require 'search_vec_original.cgi';
require 'Common.cgi';

use strict;
use Encode;
use utf8;

use CGI;
my $q = new CGI;

use File::Basename;

use KyotoCabinet;
my $title_db = new KyotoCabinet::DB;
my $title_file = 'title.kch';

main();

sub main
{
    my $file = $ARGV[0];
    my $str = decode_utf8($ARGV[1]);

    print_html::header();

    print_detail($file, $str, 0);

    print_similarity($file, $str);

    print_html::fotter();
}

sub print_detail {
    my ($file, $query, $sim) = @_;

    my @queries = split(':', $query);

    $title_db->open($title_file, $title_db->OREADER);
    my $title = $title_db->get(basename($file));
    $title = decode_utf8($title);
    $title_db->close();

    #my $title = extractTitle($file);
    foreach my $query (@queries) {
        $title =~ s/$query/<font color="red">$query<\/font>/g;
    }

    print '<div class="index_study">';
     if ($sim) {
         my $url = "view_original.cgi?$file+$query";
         print encode_utf8("<a href=$url><h3>$title</h3></a><p>")
     } else {
         print encode_utf8("<h3>$title</h3><p>");
     }

    # 本文を取得
    my @sentence = getSentence($file);
    foreach my $sent (@sentence) {
        foreach my $query (@queries) {
            $sent =~ s/$query/<font color="red">$query<\/font>/g;
        }
    }

    my $num = 1;
    foreach my $sent (@sentence) {
        if ($num == $sim) {
            last;
        } else {
            print encode_utf8("$sent\n");
        }
        $num++;
    }
    print '</p></div>';
}

sub print_similarity {

    my ($file, $str) = @_;
print << 'HERE';
    <div id="contents" class="theme-blue"> 
    <div id="index_studies">
    <br>
    <h1>類似記事</h1><br>
HERE
    my %sim = similarity::get($file);
    my @sim_rank = hash_value::sort(\%sim);
    for (my $rank = 1; $rank < 4; $rank++) {
        print_detail($sim_rank[$rank], $str, 3);
    }

}

sub getSentence {
    my($file) = @_;

    open(IN,$file) || die "Can't open $file\n";

    my @Sentence;

    while(my $line_utf8 = <IN>) {
        my $line = decode_utf8($line_utf8); 
        chomp($line);

        my @element = split(/ /,$line);
        my $tag = $element[0];

        # 先頭にタグがある行を除去
        if($tag eq "<id>" || $tag eq "<date>" || $tag eq "<title>") {
            next;
        }

        $line =~ s/^　//;  # 先頭の全角スペースを除去
        $line =~ s/^ //;   # 先頭の半角スペースを除去

        # 何もない行を除去
        if($line eq "") {
            next;
        }

        undef @element;

        push(@Sentence,$line);
    }
    close(IN);

    return @Sentence;
}


