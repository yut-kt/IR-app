#!/usr/bin/perl 
require 'CommonHtml.cgi';

use strict;
use Encode;
use utf8;

use File::Find;
use File::Basename;

use CGI;
my $q = new CGI;

use File::HomeDir;
my $home = File::HomeDir->users_home('vagrant');

main();

sub main()
{
    print_html::header();

    my $query = decode_utf8($q->param('keyword'));
    my @result = easy_search($query);

    print "<ul>";
    foreach my $file (@result) {
        my $url = "view_doc.cgi?$file";
        my $b_name = basename($file);

        print encode_utf8("<li>・<a href=$url>$b_name</a></li>\n");
    }
    print "</ul>";

    print_html::fotter();
}

sub easy_search {
    my($query) = @_;

    my $object_dir = $home . '/Nikkei/';

    my @FILES;
    find( sub{ push(@FILES,$File::Find::name) if(-f $_); }, $object_dir);

    my @result;

    foreach my $file (sort @FILES) {
        my @sentence = getSentence($file);

        foreach my $sent (@sentence) {
            if($sent =~ $query) {
                push(@result,$file);
                last;
            }
        }
    }
    undef @FILES;

    return @result;
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


        if($tag eq "<id>" || $tag eq "<date>" || $tag eq "<title>") {
            next;
        }

        $line =~ s/^　//;  # 先頭の全角スペースを除去
        $line =~ s/^ //;   # 先頭の半角スペースを除去

        if($line eq "") {
            next;
        }
        undef @element;

        push(@Sentence,$line);
    }
    close(IN);

    return @Sentence;
}


