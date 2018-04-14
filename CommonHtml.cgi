#! /usr/bin/perl
package print_html;

sub header
{
    my $request = $ENV{'REQUEST_URI'};
    my $url = "http://" . $ENV{'HTTP_HOST'} . $request;
    print << "HERE";

<!DOCTYPE html>
<html>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" href="css/lalab.css" type="text/css">
<title>EasySearch</title>
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
   <form method=post action="search_original.cgi?0">
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
<br>

HERE

}

sub fotter
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

1;
