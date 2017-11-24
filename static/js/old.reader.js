d3.json(topicsurl, function(cdata) {
    var tophtml = '<br><ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    topichtml = '<br><p>Discipline</p><ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    var tabnum = 0;
    for (k in cdata['topics']) {
        tabnum = tabnum + 1;
        var k_data = cdata['topics'][k];
        tophtml = tophtml + '<li><a href="#vtab' + tabnum + '" data-toggle="tab"><input type="checkbox" name="x" id="input-10a" value="1" data-toggle="checkbox-x"> ' + k_data + '</a></li>';
        }

    tophtml = tophtml + '</ul>';
    $(tophtml).appendTo('#topics');
});

d3.json(apiurl, function(data) {
    console.log(data);
    var polhtml = '<br><ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    for (k in data) {
        var k_data = data[k];
        console.log(k_data);
        for (d in k_data) {
                console.log(d, k_data[d]);
                var value = k_data[d];
                if (!value) {
                        value = '';
                }
                name = "<a href='" + polurl + d + "'>" + d + "</a>";
                polhtml = polhtml + '<li><b>' + value + '</b>' + name + '</li>';
        };
    };
  polhtml = polhtml + "</ul>";
  $(polhtml).appendTo('#policies');
});

d3.json(contentsurl, function(cdata) {
    var conthtml = '<br><ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    topichtml = '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    var tabnum = 0;
    var known = new Object();
    for (k in cdata['contents']) {
        tabnum = tabnum + 1;
        var k_data = cdata['contents'][k];
        if (!k_data) {
            if (tabnum == 1)
            {
                conthtml = conthtml + '<li class="active"><a href="#vtab1" data-toggle="tab">' + k + '</a></li>';
            }
            else
            {
                conthtml = conthtml + '<li><a href="#vtab' + tabnum + '" data-toggle="tab">' + k + '</a></li>';
            }
        }
        else
        {
	    var thisval = known[k_data];
            if (tabnum == 1)
            {
		if (!thisval) {
                conthtml = conthtml + '<li class="active"><a href="#vtab1" data-toggle="tab">' + k_data + '</a></li>';
		};
                topichtml = topichtml + '<li class="active"><a href="#vtab' + tabnum + '" data-toggle="tab">' + k + '</a></li>';
            }
            else
            {
		if (!thisval) {
                conthtml = conthtml + '<li><a href="#vtab' + tabnum + '" data-toggle="tab">' + k_data + '</a></li>';
		};
                topichtml = topichtml + '<li><a href="#vtab' + tabnum + '" data-toggle="tab">' + k + '</a></li>';
            }
	    known[k_data] = k;
        }
    }
    conthtml = conthtml + "</ul>";
    topichtml = topichtml + '</ul>';
    $('#community').append(conthtml);

    $(topichtml).appendTo('#discipline');
});
