var val = [];
var postdata = {};
var senddata = {};
var testdata = {};
apiurl = "/parthenos-wizard/webfilter";

y= "discipline:SOCIAL SCIENCE";
testdata[y] = 1;
var senddata =  JSON.stringify(testdata);

d3.json(topicsurl, function(cdata) {
    var tophtml = '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    topichtml = '<p>Discipline</p><ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    var tabnum = 0;
    if (cdata) {
        for (k in cdata['order']) {
	tophtml + '<p><input type="checkbox" value="topic:' + k_data + '" id="input-10a" data-toggle="checkbox-x"> ' + k + '</p>';
	for (x in cdata['topics'][k]) {
            tabnum = tabnum + 1;
            var k_data = cdata['topics'][k][x];
            tophtml = tophtml + '<p><input type="checkbox" value="topic:' + k_data + '" id="input-10a" data-toggle="checkbox-x"> ' + k_data + '</p>';
        }
	}
    }

    tophtml = tophtml + '</ul>';
})
.header("Content-Type","application/json")
.send("POST",senddata);

d3.json(principlesurl, function(pdata) {
    console.log(pdata['principles']);
  var polhtml = '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well"><table>';
  for (k in pdata['principles']) {
	stringhtml = '<tr valign=top style="border-bottom: 1px solid #000;padding-top: 5px;padding-bottom: 5px; ">';
	for (item in pdata['principles'][k]) {
	   stringhtml = stringhtml + '<td>' + pdata['principles'][k][item] + "</td><td width='8'>&nbsp;</td>\n"; 
	}
	polhtml = polhtml + stringhtml + "</tr>\n";
  }
  polhtml = polhtml + "</table></ul>";
  $("#principles").empty();
  $("#principles").html("<h4><b>PARTHENOS Guidelines</b></h4>");
  $(polhtml).appendTo('#principles');
});

function cleanup () {
    var topicdefault = '';

    d3.json(contentsurl, function(cdata) {
    var showcommunity = '<h4><b>Select your Community</b></h4><div class="tab-pane active" id="godiscipline" style="float:right"><a class="btn btn-primary btnNext">Next</a></div><br /><br />';
    var showcommunity = '';

    disciplinehtml = '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    var tabnum = 0;
    var known = new Object();
    for (k in cdata['contents']) {
        tabnum = tabnum + 1;
        var k_data = cdata['contents'][k];
        if (!k_data) {
            conthtml = '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well"><p><input name="disc" type="checkbox" value="discipline:' + k + '" id="input-10a" data-toggle="checkbox-x"> ' + k + '</p></ul>';
	    showcommunity = showcommunity + conthtml;
        }
        else
        {
            var thisval = known[k_data];
            if (!thisval) {
                disciplinehtml = disciplinehtml + '<p>&nbsp;&nbsp;<b>' + k_data + '</b></p>';
            };
            disciplinehtml = disciplinehtml + '<p><input name="disc" type="checkbox" value="discipline:' + k + '" id="input-10a" data-toggle="checkbox-x"> ' + k + '</p>';
            known[k_data] = k;
        }
    }

    disciplinehtml = disciplinehtml + '</ul>';
    showcommunity = disciplinehtml + showcommunity;

    $("#communityload").empty();
    $("#topicdata").empty();
    $("#policydata").empty();
    $('#communityload').html(showcommunity);
    topichtml = topicdefault; 
    $("#topicdata").html(topichtml);
    });
}

function makeempty () {
   $("#topics").empty();
   d3.json(topicsurl, function(cdata) {
        var tophtml = '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
        topichtml = '<br><p>Discipline</p><ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
        var tabnum = 0;
        var topics= {};
        var topicid = 0;
        for (showtopic in cdata['topics'])
        {
           topics[showtopic] = topicid;
           topicid = topicid + 1;
        }
        for (k in cdata['order']) {
                showtopic = cdata['order'][k];
                tophtml = tophtml + '<p><b><font color=#3077e8>' + showtopic + '</font></b></p>';
                topicid = topics[showtopic];
                for (x in cdata['topics'][showtopic])
                {
                tabnum = tabnum + 1;
                var k_data = cdata['topics'][showtopic][x];
                tophtml = tophtml + '<p><input type="checkbox" value="topic:' + k_data + '" id="input-10a" data-toggle="checkbox-x"> ' + k_data + '</p>';
                }
        }

        tophtml = tophtml + '</ul>';
   })
   .header("Content-Type","application/json")
   .send("POST",senddata);
   $("#policydata").empty();
}

function result (cdata, flag) {
var postdata = {};
var xcdata = ["community:RESEARCH COMMUNITY", "discipline:SOCIAL SCIENCE", "topic:LEGAL FRAMEWORK", "topic:PRIVACY AND SENSITIVE DATA"];
for (name in cdata) {
	postdata[cdata[name]] = 1;	
};

var senddata = JSON.stringify(postdata);

flag = 1;
if (flag == 1) {
	d3.json(topicsurl, function(cdata) {
    	var tophtml = '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    	topichtml = '<br><p>Discipline</p><ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    	var tabnum = 0;
	var topics= {};
	var topicid = 0;
	for (showtopic in cdata['topics'])
	{
	   topics[showtopic] = topicid;
	   topicid = topicid + 1;
	}
    	for (k in cdata['order']) {
		showtopic = cdata['order'][k];
		tophtml = tophtml + '<p><b><font color=#3077e8>' + showtopic + '</font></b></p>';
		topicid = topics[showtopic];
		for (x in cdata['topics'][showtopic])
		{
        	tabnum = tabnum + 1;
        	var k_data = cdata['topics'][showtopic][x];
        	tophtml = tophtml + '<p><input type="checkbox" value="topic:' + k_data + '" id="input-10a" data-toggle="checkbox-x"> ' + k_data + '</p>';
		}
        }

    	tophtml = tophtml + '</ul>';
    	$('#topicsdata').empty();
    	$(tophtml).appendTo('#topicsdata');
	})
	.header("Content-Type","application/json")
	.send("POST",senddata);
};

d3.json(apiurl, function(data) {
    console.log(data);
  $("#policydata").empty();
  $("#policydata").html("<img src='/parthenos-wizard/static/loading.gif'>");
  $(polhtml).appendTo('#policydata');
    var polhtml = '';
    var firstvalue = '';
    for (thistopic in data['topics']) {
	var found = 0;
	if (thistopic)
	{
            polhtml = polhtml + '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
            polhtml = polhtml + "<h2><font color=#3077e8>" + thistopic + "</font></h2>";
            console.log('Data:');
            console.log(topicdata);
	}

	var subtopics = data['topics'][thistopic];
	var firstvalue = 1;

	for (topid in subtopics)
        {
	    var subtopic = subtopics[topid];
	    var found = 0;
	    polhtml = polhtml + "<h4><font color=#3077e8>" + subtopic + "</font></h4>";
	    var topicdata = data['result'][subtopic];
	    if (topicdata) {
	       for (kindex in topicdata) 
	        {
	        keytopic = topicdata[kindex];
	        k_data = topicdata[kindex];
		if (k_data)
		{
                	var value = k_data;
                	if (!value) {
                            value = '';
                	}
			polurl = "#";
			if (k_data['policy link'])
			{
		   	    polurl = k_data['policy link'];
			    found = 1;
			}

			if (k_data['policy'])
			{
                    	    name = "<a href='" + polurl + "' target=_blank>" + k_data['policy']  + "</a>";
                    	    polhtml = polhtml + '<li>' + k_data['organisation'] + ' ' + name + '</li>';
			}
        	};
	     }
	   };

	   if (!found)
	   {
		    var keytopic = subtopic;
            	    polhtml = polhtml + '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';

		    if (data['other'])
	    	    {
	        	polhtml = polhtml + "No results for this topic.";
			polhtml = polhtml + " Here you can find some suggestions from other disciplines:";
	        	for (thisdisc in data['other'][keytopic]) 
			{
		    	    polhtml = polhtml + "<h5>" + thisdisc + "</h5>";
	 	    	    var polvalue = data['other'][keytopic][thisdisc];
	             	    for (d in polvalue)
		    	    {
				k_data = polvalue[d];
                		polurl = "#";
                		if (k_data['policy link'])
                		{  
                   	    	    polurl = k_data['policy link'];
                		}
	        		name = "<a href='" + polurl + "' target=_blank>" + k_data['policy']  + "</a>";
				if (polurl.length > 3) {
                		polhtml = polhtml + '<li> ' + k_data['organisation'] + ' ' + name + '</li>';
				}
	            	     }
			};
	    	    };

		polhtml = polhtml + "</ul>";
	     };
	 };
	 polhtml = polhtml + "</ul>";
    };
    $("#policydata").empty();
    $("#policydata").html("<h4><b>Policies that match your selection</b></h4><div><a class=\"btn btn-primary pull-left\" data-toggle=\"modal\" data-target=\"#myModal\">Suggest new policy</a></div><div class=\"tab-pane active\" style=\"float:right\"><a class=\"btn btn-primary btnNext\">Next</a></div>");
    $(polhtml).appendTo('#policydata');
})
.header("Content-Type","application/json")
.send("POST",senddata);
};

d3.json(contentsurl, function(cdata) {
    var conthtml = '<h4><b>Select your Community</b></h4><div class="tab-pane active" id="godiscipline" style="float:right"><a class="btn btn-primary btnNext">Next</a></div><br /><br />';
    var conthtml = '';

    topichtml = '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well">';
    var tabnum = 0;
    var known = new Object();
    for (k in cdata['contents']) {
        tabnum = tabnum + 1;
        var k_data = cdata['contents'][k];
        if (!k_data) {
	    conthtml = conthtml + '<ul id="nav-tabs-wrapper" class="nav nav-tabs nav-pills nav-stacked well"><p><input name="disc" type="checkbox" value="discipline:' + k + '" id="input-10a" data-toggle="checkbox-x"> ' + k + '</p></ul>';
        }
        else
        {
	    var thisval = known[k_data];
	    if (!thisval) {
		topichtml = topichtml + '<p>&nbsp;&nbsp;<b>' + k_data + '</b></p>';
	    };
            topichtml = topichtml + '<p><input name="disc" type="checkbox" value="discipline:' + k + '" id="input-10a" data-toggle="checkbox-x"> ' + k + '</p>';
	    known[k_data] = k;
        }
    }
    topichtml = topichtml + '</ul>';
    conthtml = topichtml + conthtml;
    $("#communityload").empty();
    $('#communityload').html(conthtml);

});

$(function() {
$(document).on("click", '#communityload input:checkbox', function() {
    var group = ":checkbox[name='disc']";
    if($(this).is(':checked')){
       $(group).not($(this)).attr("checked",false);
    }
});
  });

$(function() {
$(document).on("click", '#community input:checkbox', function() {
    var group = ":checkbox[name='comm']";
    if($(this).is(':checked')){
       $(group).not($(this)).attr("checked",false);
    }
});
  });

$(function() {
$(document).on("click", '#discipline input:checkbox', function() {
    var group = ":checkbox[name='disc']";
    if($(this).is(':checked')){
       $(group).not($(this)).attr("checked",false);
    }
});
  });
