#!/usr/bin/perl
require 'CommonHtml.cgi';

use strict;
use Encode;
use utf8;

use CGI;
my $q = new CGI;

main();

sub main
{
    my $file = $ARGV[0];
    my $test = $ARGV[1];

    print_html::header();
    print $test;

    my $title = extractTitle($file);

    print '<div class="index_study">';
    print encode_utf8("<h3>$title</h3><p>\n");

    # 本文を取得
    my @sentence = getSentence($file);
    foreach my $sent (@sentence) {
        print encode_utf8("$sent\n");
    }

    print '<p></div>';

    print_html::fotter();
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

sub extractTitle {
    my($file) = @_;

    open(SGML, $file) || die "Can't open $file\n";

    my $data;
    while(my $line_utf8 = <SGML>) {
        my $line = decode_utf8($line_utf8);
        chomp($line);

        my($tag, $data) = split(/ /,$line);
        if($tag eq "<title>") {
            return $data;
        }
    }
    close(SGML);
}



