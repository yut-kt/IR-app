#!/usr/bin/perl
package hash_value;

use strict;
use Encode;
use utf8;

use CGI;
my $q = new CGI;


# --------- ハッシュのvalueでソート -----------
# 引数 : ハッシュのリファレンス
# 戻値 : ソートされた順番にキーが格納された配列
# 使用方法 : @keys = sort_hash_value(\%Hash);
sub sort {
   my ($ref_hash) = @_;
   my (@keys);
   @keys = sort { $$ref_hash{$b} <=> $$ref_hash{$a} } keys %{$ref_hash};
   return @keys;
}

