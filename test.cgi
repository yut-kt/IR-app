#!/usr/bin/perl 

use strict;
use Encode;
use utf8;

use File::Find;
use File::Basename;

use CGI;
my $q = new CGI;

main();

sub main()
{
    print_html_header();

    # 検索キーワードを取得
    my $query = decode_utf8($q->param('keyword'));

    # 検索エンジン（too_easy.pl）
    my @result = easy_search($query);

    # 検索結果を表示
    print "<ul>\n";
    foreach my $file (@result)
    {
	my $url = "view_doc.cgi?$file";
	my $b_name = basename($file);

	print encode_utf8("<li>・<a href=$url>$b_name</a></li>\n");
    }
    print "</ul>\n";

    print_html_fotter();

}

sub easy_search
{
    # 検索キーワード
    my($query) = @_;

    # 記事の格納されているディレクトリ
    my $home = "/data/share";
    my $object_dir = $home."/Nikkei/";

    # ディレクトリに含まれるファイル(サブディレクトリも含む)のフルパスを得る
    # (ファイルのフルパスは@FILES に格納)
    my @FILES;
    find( sub{ push(@FILES,$File::Find::name) if(-f $_); }, $object_dir);

    my @result;

    foreach my $file (sort @FILES)
    {
	my @sentence = getSentence($file);

	foreach my $sent (@sentence)
	{
	    if($sent =~ $query)
	    {
		push(@result,$file);
		last;
	    }
	}
    }
    undef @FILES;

    return @result;
}


# 機能：引数で指定した新聞記事ファイルの本文を取り出す
# 引数
#  - $file：ファイル
# 戻値：本文を格納したリスト
sub getSentence
{
    my($file) = @_;

    # ファイルをオープン
    open(IN,$file) || die "Can't open $file\n";

    my @Sentence;

    while(my $line_utf8 = <IN>)
    {
	my $line = decode_utf8($line_utf8); 
	chomp($line);

	my @element = split(/ /,$line);
	my $tag = $element[0];

	# 先頭にタグがある行を除去
	if($tag eq "<id>" || $tag eq "<date>" || $tag eq "<title>")
	{
	    next;
	}

	$line =~ s/^　//;  # 先頭の全角スペースを除去
	$line =~ s/^ //;   # 先頭の半角スペースを除去

	# 何もない行を除去
        if($line eq "")
	{
	    next;
	}

	undef @element;

	push(@Sentence,$line);
    }
    close(IN);

    return @Sentence;
}


sub print_html_header
{
    print << "HERE";

<!DOCTYPE html>
<html>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" href="css/lalab.css" type="text/css">
<title>EasySearchs</title>
</head>

<body>

<!-- Header -->
<div id="header">
<div id="lab-name">Information Retrieval</div>
</div>

<!-- Input field -->
<div id="contents" class="theme-blue padding-none">
  <div id="index_intro">

   <table width="75%">
   <tr><td>　</td></tr>
   <tr><td align="center">
   <form method=post action="easy_search.cgi?0">
     <input type=text name="keyword" size=50>
     <input type=submit value="検索">
     <input type=reset value="クリア">
   </form>
   </td></tr>
   </table>

  </div>
</div>

<div id="contents" class="theme-blue"> 
<div id="index_studies">

HERE
}

sub print_html_fotter
{
    print << "HERE";

</div>
</div>

<!-- fotter -->
<div id="fotter">
  <div><a href="http://www.ci.seikei.ac.jp/sakai/">Language Information Laborato
ry</a></div>
</div>

</body>
</html>

HERE

}
