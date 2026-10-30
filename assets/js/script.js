// google.load("search", "1");

/*
function OnLoad() {
    // Create a search control
    var searchControl = new google.search.SearchControl();

    // Create a Web Search
    var webSearch = new google.search.WebSearch();

    // Set the Search Control to get the most number of results
    searchControl.setResultSetSize(google.search.Search.LARGE_RESULTSET);

    // Restrict our search to pages from Weld Engineering
    webSearch.setSiteRestriction('www.weldengineering.com');

    // web search, open, alternate root
    var options = new google.search.SearcherOptions();
    options.setExpandMode(google.search.SearchControl.EXPAND_MODE_OPEN);
    options.setRoot(document.getElementById("cse"));
    searchControl.addSearcher(webSearch, options);

    // Set No Result String
    options.setNoResultsString("<center>Your search query did not return any results.  Please check your spelling and try again.<\/br>You may also have to try removing quotes or other punctuation and operators.<\/center>");

    // Make Open On Same Page
    webSearch.setLinkTarget("_self");

    // Tell the searcher to draw itself and tell it where to attach
    searchControl.draw(document.getElementById("searchcontrol"));

}
*/

// google.setOnLoadCallback(OnLoad);

function reshow(e) {
    var a = document.getElementById(e);
    var b = "#" + e;
    var maxhh = 45;
    var ahigh = $(b).height();
    var whigh = $(window).height();
    var scrol = $(window).scrollTop();
    var toppp = (whigh - ahigh) / 2 + scrol;
    var toppity = toppp + "px";
    var along = $(b).width();
    var wwide = $(window).width();
    var leftt = (wwide - along) / 2;
    var leftity = leftt + "px";
    var dhigh = $(document).height() + "px";
    var clsrl = scrol + "px";
    $("#fade").css("display", "block");
    $("#fade").css("height", dhigh);
    $(b).css("display", "block");
    $(b).css("position", "absolute");
    $(b).css("marginLeft", "0px");
    if (toppp < maxhh) {
        toppity = maxhh + "px";
    }
    $(b).css("top", toppity); 
    $(b).css("left", leftity);
}

function show(e) {
    var a = document.getElementById(e);
    var b = "#" + e;
    var maxhh = 45;
    var ahigh = $(b).height();
    var whigh = $(window).height();
    var scrol = $(window).scrollTop();
    var toppp = (whigh - ahigh) / 2 + scrol;
    var toppity = toppp + "px";
    var along = $(b).width();
    var wwide = $(window).width();
    var leftt = (wwide - along) / 2;
    var leftity = leftt + "px";
    var dhigh = $(document).height() + "px";
    var clsrl = scrol + "px";
    if (a.style.display === "block") {
        $("#fade").css("display", "none");
        $(b).css("display", "none");
        var mbot = whigh - maxhh - 27;
        var mbo = mbot + "px";
        $("#newlb").css("bottom", mbo);
        $("#newlb").css("left", "50%");
        var mleft = along / 2 - 50;
        var mlef = mleft + "px";
        $("#newlb").css("margin-left", mlef);
        $("#newlb").css("display", "block");
        $("#newlb").animate({
            marginLeft: '0px',
            left: '0px',
            bottom: '0px'
        }, 250);
    } else {
        $("#fade").css("display", "block");
        $("#fade").css("height", dhigh);
        $(b).css("display", "block");
        $(b).css("position", "absolute");
        $("#newlb").css("display", "none");
        if (e !== "search" && e !=="prodsel") {
            $(".clseimg").css("display", "block");
            $(".clseimg").css("top", clsrl);
            if (toppp < maxhh) {
                toppity = maxhh + "px";
            }
            $(b).css("top", toppity); 
            $(b).css("left", leftity);
            if (e === "lightbox") {
            }
        } else {
            $(".clseimg").css("display", "none");
        }
    }
}

function showtb(e) {
    var a = document.getElementById(e);
    var b = "#" + e;
    if (a.style.display === "block") {
        $(b).css("display", "none");
    } else {
        $(b).css("display", "block");
    }
}

function printpic(elmnt1, elmnt2) {
    document.open();
    document.write('<html><head><title>Weld Engineering, Co. - ');
    document.write(elmnt1);
    document.write('<\/title><style type="text/css" media="screen">@import url( includes/printimg.css );<\/style><link href="includes/printimg4print.css" type="text/css" rel="stylesheet" media="print"><center><div id="printheader"><img src="images/header.png" alt="Weld Engineering Header"><\/div><\/center><h1 style="text-align:center;font-family:Arial;">');
    document.write(elmnt1);
    document.write('<\/h1><link href="includes/print.css" type="text/css" rel="stylesheet" media="print"><\/head><body><center><img src="images/');
    document.write(elmnt2);
    document.write('" style="position:relative;top:-10px;"><br><span class="noprint"><a href="');
    document.write(window.location.href);
    document.write('">BACK<\/a> | <a href="#" onclick="window.print();return false;">PRINT<\/a><\/span><\/center><\/body><\/html>');
    document.close();
}

function printpng(elmnt1, elmnt2) {
    document.open();
    document.write('<html><head><title>Weld Engineering, Co. - ');
    document.write(elmnt1);
    document.write('<\/title><style type="text/css" media="screen">@import url( includes/printimg.css );<\/style><link href="includes/printimg4print.css" type="text/css" rel="stylesheet" media="print"><center><div id="printheader"><img src="images/header.png" alt="Weld Engineering Header"><\/div></center><h1 style="text-align:center;font-family:Arial;">');
    document.write(elmnt1);
    document.write('<\/h1><link href="print.css" type="text/css" rel="stylesheet" media="print"><\/head><body><center><img src="tb708/');
    document.write(elmnt2);
    document.write('" style="position:relative;top:-10px;"><br><span class="noprint"><a href="');
    document.write(window.location.href);
    document.write('">BACK<\/a> | <a href="#" onclick="window.print();return false;">PRINT<\/a><\/span><\/center><\/body><\/html>');
    document.close();
}

function high(elemnt) {
    var a = document.getElementById(elemnt);
    a.style.color = 'red';
}

function low(elemnt) {
    var a = document.getElementById(elemnt);
    a.style.color = 'blue';
}

var cst = 0;
var wld = 0;
var mtl = 0;
var flx = 0;
var lbr = 0;
var hrs = 0;

function calculate() {
    var rcvrstr = document.CALCULATOR.rcvr.options[document.CALCULATOR.rcvr.selectedIndex].value;
    var rcvr = rcvrstr.split("--");
    var ynr = rcvr[1]; // If manually recovering flux or not. 1 = disposed, 0 = recovered.
    var mtl = document.CALCULATOR.metal.value * ynr; // Weld metal deposited per week.
    var cst = document.CALCULATOR.ecost.value; // Equipment cost.
    var fur = document.CALCULATOR.mult.value; // Flux utilization ratio.
	var wld = fur - 1; // Assumes 1:1 metal to slag ratio.
    var flx = document.CALCULATOR.flux.value; // Cost of flux per pound.
    var lbr = document.CALCULATOR.labor.value; // Labor + burden rate, $/hr.
    var hrs = document.CALCULATOR.hours.value; // Hours of labor per week.
	var wks = 50; // Weeks in a year, accounting for 2 weeks of holidays.
	if (ynr === "1") {
		var flxsvd = Math.round(wld * mtl * wks) + " Lbs. of Flux Saved per Year";
	} else {
		var flxsvd = "(No Additional Flux Recovered)";
	}
	var lbrsvd = Math.round(hrs * wks) + " Hrs. of Labor Saved per Year";
	var svd0 = Math.round(wld * mtl * flx * wks + lbr * hrs * wks - cst) + " Saved in First Year";
	var svd1 = Math.round(wld * mtl * flx * wks + lbr * hrs * wks) + " Saved Each Year After";
	var roi = cst / ( wld * mtl * flx * wks + lbr * hrs * wks );
	if (roi >= 1) {
			var roiy = " (" + ( Math.round( roi * 10 ) / 10 ) + " yr ROI)";
			var roim = "";
	} else {
		var roiy = "";
		var roim = " (" + ( Math.round( roi * 120 ) / 10 ) + " mo ROI)";
	}
	var svdh = flxsvd + "<br>" + lbrsvd + "<br>&dollar;" + svd0 + "<i>" + roim + "</i><br>&dollar;" + svd1 + "<i>" + roiy + "</i>";
	var svda = flxsvd + "\n" + lbrsvd + "\n" + "$" + svd0 + roim + "\n" + "$" + svd1 + roiy;
    if (document.all) {
        document.all["writeto"].innerHTML = svdh;
    } else if (document.getElementById) {
        document.getElementById("writeto").innerHTML = svdh;
    } else {
        alert(svda);
    }

}


function clear1() {
    if (document.all) {
        document.all["writeto"].innerHTML = "&nbsp;";
    } else if (document.getElementById) {
        document.getElementById("writeto").innerHTML = "&nbsp;";
    } else {
        alert("Please upgrade your browser to Firefox 3.0, Internet Explorer 8.0, Google Chrome, Safari, Opera 9, or to the latest current version of those.");
    }

}

var addthis_options = 'slashdot, technorati, delicious, diigo, twitter, digg, stumbleupon, reddit, linkedin, google, newsvine, facebook, more';
var addthis_exclude = 'print, email, favorites';

function boothpop() {
    window.open("booth.png", "BoothPopUp", "status = 1, height = 670, width = 1182, resizable = 0");
}

function labor(lbs) {
	// This sigmoidal equation simulates a curve whereby 250 lbs/wk is 2.5 hrs/wk, 1000 lbs/wk is 3.25 hrs/wk, and 70,000 lbs/wk is 40 hrs/wk.
	var siginsstr = document.CALCULATOR.sigmoidalinputs.value;
    var sigins = siginsstr.split("--");
    var bota = parseFloat(sigins[0]);
    var topa = parseFloat(sigins[1]);
    var flxp = parseFloat(sigins[2]);
    var slpe = parseFloat(sigins[3]);
	var lbsf = parseFloat(lbs);
    return Math.round( ( bota + ( topa - bota ) / ( 1 + Math.pow( 10 , ( flxp - Math.log( lbsf ) ) * slpe ) ) ) * 4 ) / 4;
}

function recalcd(ch) {
    var equipstr = document.CALCULATOR.equip.options[document.CALCULATOR.equip.selectedIndex].value;
    var equip = equipstr.split("--");
    var rcvrstr = document.CALCULATOR.rcvr.options[document.CALCULATOR.rcvr.selectedIndex].value;
    var rcvr = rcvrstr.split("--");
    var mtl = equip[0]; // Pounds of metal deposited per week.
    var cst = equip[1]; // Cost of equipment.
    var wld = document.CALCULATOR.weld.options[document.CALCULATOR.weld.selectedIndex].value; // Flux utilization multiplier.
    var lbrm = rcvr[0]; // Recovered vs. disposed labor multiplier.
    var hrs = parseFloat(labor( mtl * wld )) * lbrm; // Labor per week.
    document.CALCULATOR.metal.value = mtl;
    document.CALCULATOR.ecost.value = cst;
    document.CALCULATOR.mult.value = wld;
    document.CALCULATOR.hours.value = hrs;
}