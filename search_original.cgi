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

use File::Basename;

my $N = 188627;

main();

sub main
{
    print_html::header();

    my $query = decode_utf8($q->param('keyword'));
    my @queries = split(' ', $query);

    my %count;

    # open DB
    $index_db->open($index_file, $index_db->OREADER);
    my %tfidf;
    foreach my $query (@queries) {
        # get file_url
        my $result_str = $index_db->get($query);
        my @result_list = split(',', $result_str);
        my $df = @result_list;

        foreach my $file (sort @result_list) {
            my ($name, $tf) = split(':', $file);
            $count{$name}++;
            $tfidf{$name} += $tf * log($N / $df) / log(2);
        }
    }
    # close DB
    $index_db->close();

    # sort hash
    my @sorted_file_list = hash_value::sort(\%tfidf);

    $query =~ s/ |　/:/g;

    print << "HERE";
<form method=post type=checkbox action='select_feedback.cgi?0'>
    <input type="hidden" name="query" value=$query>
    <input type="submit" value="フィードバック">
    <br>
    <br>
    <ul>
HERE

    # open DB
    $title_db->open($title_file, $title_db->OREADER);
    my $rank = 0;
    foreach my $key (@sorted_file_list) {
        if ($count{$key} == $#queries + 1) {
            my $url = "view_original.cgi?$key+$query";
            my $title = decode_utf8($title_db->get(basename($key)));
            $rank++;
            print << "HERE";
        <li>
            <input type="checkbox" name="check" value=$key>
            <a href=$url>$rank --> $title</a>
            <br>
            (TF-IDF : $tfidf{$key})
        </li>
        <br>

HERE
        }
    }
    # close DB
    $title_db->close();

    print << 'HERE';
    </ul>
</form>
HERE

    print_html::fotter();

    undef @sorted_file_list;
    undef %tfidf;

}

