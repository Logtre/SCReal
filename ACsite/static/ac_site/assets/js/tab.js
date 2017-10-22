$(function() {
	    //クリックしたときのファンクションをまとめて指定
	    $('.tab .toggle').click(function() {

	        //.index()を使いクリックされたタブが何番目かを調べ、
	        //indexという変数に代入します。
	        var index = $('.tab .toggle').index(this);

	        //コンテンツを一度すべて非表示にし、
	        $('.content .toggle').css('display','none');

	        //クリックされたタブと同じ順番のコンテンツを表示します。
	        $('.content .toggle').eq(index).css('display','block');

	        //一度タブについているクラスselectを消し、
	        $('.tab .toggle').removeClass('select');

	        //クリックされたタブのみにクラスselectをつけます。
	        $(this).addClass('select')
	    });
	});
