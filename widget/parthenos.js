d3.json(contentsurl, function(cdata) {
    var conthtml = '<br><ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    topichtml = '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    var tabnum = 0;
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
            if (tabnum == 1)
            {
                conthtml = conthtml + '<li class="active"><a href="#vtab1" data-toggle="tab">' + k_data + '</a></li>';
                topichtml = topichtml + '<li class="active"><a href="#vtab' + tabnum + '" data-toggle="tab">' + k + '</a></li>';
            }
            else
            {
                conthtml = conthtml + '<li><a href="#vtab' + tabnum + '" data-toggle="tab">' + k_data + '</a></li>';
                topichtml = topichtml + '<li><a href="#vtab' + tabnum + '" data-toggle="tab">' + k + '</a></li>';
            }
        }
    }
    conthtml = conthtml + "</ul>";
    topichtml = topichtml + '</ul>';
    $('#target').append(conthtml);

    $(topichtml).appendTo('#discripline');
});

d3.json(topicsurl, function(cdata) {
    var tophtml = '<br><ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    topichtml = '<br><p>Discipline</p><ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    var tabnum = 0;
    for (k in cdata['topics']) {
        tabnum = tabnum + 1;
        var k_data = cdata['topics'][k];
        tophtml = tophtml + '<li><a href="#vtab' + tabnum + '" data-toggle="tab">' + k_data + '</a></li>';
        }

    tophtml = tophtml + '</ul>';
    $(tophtml).appendTo('#fair');
});
