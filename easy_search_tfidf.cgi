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
    $title_db->open($title_file, $title_db->OREADER);

    my %sum_tfidf;
    foreach my $query (@queries) {
        # get file_url
        my $result_str = $index_db->get($query);
        my @result_list = split(/\,/,$result_str);
        my $df = @result_list;

        foreach my $file (sort @result_list) {
            my ($name, $tf) = split(':', $file);
            $count{$name}++;
            $sum_tfidf{$name} += $tf * log($N / $df) / log(2);
        }
    }

    # sort hash
    my @sorted_file_list = hash_value::sort(\%sum_tfidf);

    my $rank = 1;
    print "<ul>";
    foreach my $key (@sorted_file_list) {
        if ($count{$key} == $#queries + 1) {
            my $url = "view_doc.cgi?$key";
            my $title = decode_utf8($title_db->get(basename($key)));
            print encode_utf8("<li><a href=$url>$rank --> $title</a></li><br>");
            $rank++;
        }
    }
    print "</ul>\n";
    print_html::fotter();

    undef @sorted_file_list;
    undef %sum_tfidf;

    $index_db->close();
}


