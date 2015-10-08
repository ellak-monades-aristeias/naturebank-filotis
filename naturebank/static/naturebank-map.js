function gup( name )
{
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp( regexS );
    var results = regex.exec( window.location.href );
    if( results == null )
        return "";
    else
        return results[1];
}

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,
        function(m,key,value) {
            vars[key] = decodeURI(value);
        });
    return vars;
}

Object.extend = function(destination, source) {
    for (var property in source)
        destination[property] = source[property];
    return destination;
};

var point1 = new OpenLayers.LonLat(19.3, 34.75);
var point2 = new OpenLayers.LonLat(29.65,41.8);
var bounds = new OpenLayers.Bounds();
bounds.extend(point1);
bounds.extend(point2);
bounds.transform(new OpenLayers.Projection("EPSG:4326"), new
OpenLayers.Projection("EPSG:900913"));
var map = null;
var apopup = null;
var ktimatologio = new OpenLayers.Layer.WMS("Υπόβαθρο «ΚΤΗΜΑΤΟΛΟΓΙΟ Α.Ε.»",
  "http://gis.ktimanet.gr/wms/wmsopen/wmsserver.aspx",
    {   layers: 'KTBASEMAP', transparent: false},
    {   isBaseLayer: true,
        projection: new OpenLayers.Projection("EPSG:900913"),
        iformat: 'image/png', maxExtent: bounds, numZoomLevels:
        15, units: "m", maxResolution: 900,
        attribution: ""});
var osm = new OpenLayers.Layer.OSM.Mapnik("Υπόβαθρο \"Open Street Map\"",{isBaseLayer: true,
        attribution: "Map by <a href='http://www.openstreetmap.org/'>OSM</a>"});
var ocm = new OpenLayers.Layer.OSM.CycleMap("Υπόβαθρο \"Open Cycle Map\"",{isBaseLayer: true,
        attribution: "Map by <a href='http://www.openstreetmap.org/'>OSM</a>"});
var google_hyb = new OpenLayers.Layer.Google("Google Hybrid map", {isBaseLayer:true, numZoomLevels: 20, type: google.maps.MapTypeId.HYBRID, animationEnabled:false});
var base_layers = [ocm, osm, google_hyb, ktimatologio];
function InvokePopup(tfeature) {
    if(!tfeature.cluster)
        afeature = tfeature;
    else
        afeature = tfeature.cluster[0];
    apoint = tfeature.geometry.getBounds().getCenterLonLat();
    var aprogress = new OpenLayers.Popup('Φορτώνει...', apoint, new OpenLayers.Size(72,14), 
        '<p style="font-size:8pt; margin: 2px;">Φορτώνει...</p>', false);
    aprogress.setBorder("1px solid");  
    aprogress.setBackgroundColor('#D9D9DF');
    map.addPopup(aprogress, true);
    map.panTo(apoint);
    $.get("/biotopes/b/"+afeature.attributes["id"]+'/', {}, function(data){
        var amessage = '';
        amessage=data;
        apopup = new OpenLayers.Popup(afeature.attributes["name"], apoint, new OpenLayers.Size(215,155), amessage, true);
        apopup.setBorder("2px solid");  
        apopup.setBackgroundColor('#FFEEEE');
        map.addPopup(apopup, true);
    });
}
function InvokeTooltip(element){
    var atitle='';
    if(!element.feature.cluster)
        atitle = element.feature.attributes["name"];
    else
    {
        var subelements = [];
        for(i=0; i<element.feature.cluster.length; i++)
            subelements[i] = element.feature.cluster[i].attributes["name"];
        atitle = subelements.length+' τόποι συγκεντρωμένοι σε μικρή απόσταση: '+subelements.join(', ')+
            '. Κάντε επιπλέον zoom για να διαχωριστούν.';
    }
    document.getElementById("map").title = atitle;
}
function HideTooltip(){
    document.getElementById("map").title = '';
}
function CreateLayer(AName, ObjectName, AFillColor, AStrokeColor){
    if(map_mode==1){
        var geo_code = unescape(gup('geo_code'));
        var simplify = "True";
        var acategory = gup('category');
        var single_category = "False";
        if(acategory!="")single_category = "True";
        var params = {'simplify': simplify, 'single_category': single_category};
        Object.extend(params, getUrlVars());
        delete params['category'];
        if(geo_code)params['geo_code']=geo_code;
    }
    else if(map_mode==2){
        var params = {'site_code': abiotope_site_code, 'simplify': "False"};
    }
    else if(map_mode==3){
        var params = {'species': aspecies_id, 'simplify': "True"};
    }
    else{
        var params = {'simplify': "True"};
    }
    Object.extend(params, {request: 'GetFeature', srs: 'EPSG:4326',
                           version: '1.0.0', service: 'WFS',
                           format: 'WFS'});
    var labelvalue = "";
    var labeling_opts = {
            label : labelvalue, fontColor: "#604050",
            fontSize: "9px", fontFamily: "Verdana, Arial",
            fontWeight: "bold", labelAlign: "cm" 
    };
    var general_opts = {
            pointRadius: "${radius}", fillColor:
            AFillColor, fillOpacity: 0.50, strokeColor: AStrokeColor,
            strokeWidth: 2, strokeOpacity: 0.7
    };
    general_opts = Object.extend(general_opts, labeling_opts);
    AURL = "/"+ObjectName+"/kml/";
    var alayer = new OpenLayers.Layer.Vector(AName,
    {   
        strategies: [
                     new OpenLayers.Strategy.BBOX({ratio: 1.5,
                     resFactor: 2})//,
//                     new OpenLayers.Strategy.Cluster({distance: 10,
//                     threshold: 3})
//*******There is a bug not allowing the clustering in IE *********
                     ],
        protocol: new OpenLayers.Protocol.HTTP({
                        url: AURL,
                        format: new OpenLayers.Format.KML(),
                        params: params}),
        projection: new OpenLayers.Projection("EPSG:4326"),
        formatOptions: { extractAttributes:true },
        styleMap: new OpenLayers.StyleMap({
            "default": new OpenLayers.Style(
                  OpenLayers.Util.applyDefaults(general_opts,
                        OpenLayers.Feature.Vector.style["default"]),
                        {
                            context: {
                                radius: function(feature) {
                                    if(!feature.cluster)
                                        return 20;
                                    else
                                        return Math.log(feature.attributes.count*2.1+1)+1;
                                },
                                asitecode: function(feature){
                                    if(!feature.cluster)
                                        return feature.attributes["sitecode"];
                                    else
                                        return feature.cluster[0].attributes["sitecode"];

                                }
                            }
                        }),
            "select": new OpenLayers.Style(
                  OpenLayers.Util.applyDefaults({pointRadius: "${radius}",
                        fillOpacity: 0.6, strokeColor: AStrokeColor,
                        strokeWidth: 2, strokeOpacity: 0.7},
                        OpenLayers.Feature.Vector.style["select"]))
        })
    } );
    alayer.events.register("loadstart", alayer,
        function() { ShowProgress(ObjectName); } );
    alayer.events.register("loadend", alayer,
        function() { HideProgress(ObjectName); } );
    alayer.events.register("loadcancel", alayer,
        function() { HideProgress(ObjectName); } );
    alayer.events.on({
        "featureselected": function(e) {
            InvokePopup(e.feature);
        },
        "featureunselected": function(e) {
            map.removePopup(apopup);
        }
    });
    return alayer;
}
var natura = CreateLayer("Βιότοποι Natura", "natura", '#dd0022', '#990077');
var sonbs = CreateLayer("Τοπία (ΤΙΦΚ)", "sonbs", '#00dd22', '#009977');
var othersonbs = CreateLayer("Άλλα τοπία", "othersonbs", '#0022dd', '#005599');
var corine = CreateLayer("Βιότοποι Corine", "corine", '#ddcc44', '#99551b');
var other = CreateLayer("Άλλοι Βιότοποι", "other", '#779900', '#558800');
var categories = [natura, other, corine, othersonbs, sonbs];
var categories_strs = ['natura', 'other', 'corine', 'othersonbs', 'sonbs'];
var categories_ids = [4, 0, 1, 2, 2, 3];
function CreateSettlementsLayer()
{
    var settlements = new OpenLayers.Layer.WFS('Settlements', '/settlements/', {},
    {   projection: new OpenLayers.Projection("EPSG:4326"),
        format: OpenLayers.Format.KML,
        displayInLayerSwitcher: false,
        minScale: 500000,
        formatOptions: { extractAttributes:true },
        styleMap: new OpenLayers.StyleMap({ 
            "default": new OpenLayers.Style(
                  OpenLayers.Util.applyDefaults({
                    strokeColor: "#404000", fillColor: "#ff0000",
                    pointRadius: 2, strokeOpacity: .80, fillOpacity: .60,
                    label : "${name}", fontColor: "#110000",
                    fontSize: "${asize}", fontFamily: "Verdana, Arial",
                    fontWeight: "", labelAlign: "cb"}, OpenLayers.Feature.Vector.style["default"]),
                    {
                        context: {
                            asize: function(feature) {
                                if(feature.attributes["area"]<160000)
                                    return "9px";
                                else if(feature.attributes["area"]<1000000)
                                    return "11px";
                                else if(feature.attributes["area"]<5000000)
                                    return "13px";
                                else
                                    return "15px";
                            }
                        }
                    })
        })
    } );
    return settlements;
}
var settlements = CreateSettlementsLayer(); 
function additemtolegend(layer, layername){
    legenddiv = document.getElementById("idlegend");
    if(legenddiv==null)return;
    var oldhtml = legenddiv.innerHTML;
    var newhtml = oldhtml+"<div><input type=checkbox checked name='chk"+layername+
        "' onClick='"+layername+".setVisibility(chk"+layername+".checked);'> "+
        "<div style='position: absolute; display: inline; width: 15px; height: 15px; background-color: "+
        layer.styleMap.styles["default"].defaultStyle["fillColor"]+
        "; border: 2px solid "+layer.styleMap.styles["default"].defaultStyle["strokeColor"]+";'></div>"+
        "<div style='position: relative; left: 20px; width: 80px; height: 18px; display: inline;'>"+layer.name+"</div>"+
        "<div id='progress_"+layername+"' style='position: relative; display: inline; width: 16px; left: 20px'></div></div>";
    legenddiv.innerHTML = newhtml;
}
function additemstolegend(layers, layersname){
    for(i=layers.length-1;i>=0;i--){
        additemtolegend(layers[i], layersname[i]);
    }
}
function init() {
    var options = {
        'units' :   "m",
        'numZoomLevels' :   15,
        'sphericalMercator': true,
        'maxExtent': bounds,
        'projection'    :   new OpenLayers.Projection("EPSG:9009313"),
        'displayProjection':    new OpenLayers.Projection("EPSG:4326")
    };
    map = new OpenLayers.Map('map', options);
    map.addControl(new OpenLayers.Control.ScaleLine());
    var ANavToolBar = new OpenLayers.Control.NavToolbar();
        map.addControl(ANavToolBar);
    if(map_mode!=2)
    {
        $("div.olControlNavToolbar").css("top","318px");
        $("div.olControlNavToolbar").css("left","11px");
    } else {
        $("div.olControlNavToolbar").css("top","18px");
        $("div.olControlNavToolbar").css("left","350px");
    }
    pzb = new OpenLayers.Control.PanZoomBar();
    pzb.zoomWorldIcon = false;
    map.addControl(pzb);
    map.addControl(new OpenLayers.Control.MousePosition());
    map.addControl(new OpenLayers.Control.OverviewMap());
    map.addLayer(ocm);
    map.addLayer(osm);
    map.addLayer(google_hyb);
    map.addLayer(ktimatologio);
    map.addLayer(settlements);
    var cat_id_repr ="";
    var geo_code = unescape(gup('geo_code'));
    if(map_mode==0||map_mode==3){
        additemstolegend(categories, categories_strs);
        map.addLayers(categories);
    }else if(map_mode==1){
        var acategory = gup('category');
        if(acategory!=""){
            var id_category = parseInt(acategory)-1;
            if(id_category==4)
                id_category--;
            additemtolegend(categories[categories_ids[id_category]], 
                       categories_strs[categories_ids[id_category]]);
            map.addLayer(categories[categories_ids[id_category]]);
            cat_id_repr = (++id_category)+"";
        }else{
            additemstolegend(categories, categories_strs);
            map.addLayers(categories);
        }
    }
    else if(map_mode==2){
        if(acat_id==5)
            acat_id--;
        acat_id--;
        additemtolegend(categories[categories_ids[acat_id]], 
                   categories_strs[categories_ids[acat_id]]);
        map.addLayer(categories[categories_ids[acat_id]]);
    }
    var radiogroup = document.getElementById('idbaselayers');
    if(radiogroup!=null){
        for(i=0;i<radiogroup.elements.length;i++){
            if(radiogroup.elements[i].type =="radio"){
                if(radiogroup.elements[i].checked){
                    map.setBaseLayer(base_layers[i]);
                    break;
                }
            }
        }
    }
    var asite_code='';
    if(map_mode==2)
    {
        asite_code=abiotope_site_code;
        cat_id_repr='';
    }
    var aspecies='';
    if(map_mode==3)
        aspecies=aspecies_id;
    var getboundoptions = {'site_code': asite_code, 'species': aspecies};
    Object.extend(getboundoptions, getUrlVars());
    if(cat_id_repr)getboundoptions['category']=cat_id_repr;
    if(geo_code)getboundoptions['geo_code']=geo_code;
    $.ajax({url: "/bound/", data: getboundoptions, method: 'get', 
        success: function(data){
            bounds = OpenLayers.Bounds.fromString(data);
            bounds.transform(new OpenLayers.Projection("EPSG:4326"), new
                                 OpenLayers.Projection("EPSG:900913"));
            map.zoomToExtent(bounds);
        }, 
        error: function(data){
            map.zoomToExtent(bounds);
    }});
    var SelectControl = new OpenLayers.Control.SelectFeature(categories, {
          clickout: true, togle: false, multiple: false,
          hover: false});
    var HoverControl = new OpenLayers.Control.SelectFeature(categories, {
          clickout: false, togle: false, multiple: false,
          hover: true, highlightOnly: true, renderIntent: "temporary",
          eventListeners: { beforefeaturehighlighted: function(e){},
                            featurehighlighted: function(e){InvokeTooltip(e)},
                            featureunhighlighted: function(e){HideTooltip()}
                          }});
    if(map_mode!=2)
    {
        map.addControl(SelectControl);
        map.addControl(HoverControl);
        HoverControl.activate();
        SelectControl.activate();
        ANavToolBar.controls[0].events.on({
            "activate": function(){
                HoverControl.activate();
                SelectControl.activate();
            },
            "deactivate": function(){
                HoverControl.deactivate();
                SelectControl.deactivate();
            }
        });
    }
    ANavToolBar.controls[0].activate();
    map.events.register("zoomend", map,
        function() {
            notenabled = map.getScale()>500000;
            $('#id_chksettlements').attr('disabled', notenabled);
            if(notenabled)
                $('#id_lblsettlements').addClass('disabled');
            else
                $('#id_lblsettlements').removeClass('disabled');
        }
    );
}

function ShowProgress(name){
   var aprogress = document.getElementById("progress_"+name);
   if(aprogress==null)return;
   aprogress.innerHTML=
       "<img src='"+STATIC_URL+"'/wait16.gif'>";
}

function HideProgress(name){
   var aprogress = document.getElementById("progress_"+name);
   if(aprogress==null)return;
   aprogress.innerHTML="";
}

function setLayersOpaque(value){
    for(i=0;i<categories.length;i++){
        var layer = categories[i];
        var defaultStyle = layer.styleMap.styles["default"].defaultStyle;
        if(value)
            defaultStyle["fillOpacity"]=0.6;
        else
            defaultStyle["fillOpacity"]=0;
        layer.styleMap.styles["default"].setDefaultStyle(defaultStyle);
        layer.redraw();
    }
}

function setLayersLabels(value){
    for(i=0;i<categories.length;i++){
        var layer = categories[i];
        var defaultStyle = layer.styleMap.styles["default"].defaultStyle;
        if(value)
            defaultStyle["label"]="${asitecode}";
        else
            defaultStyle["label"]="";
        layer.styleMap.styles["default"].setDefaultStyle(defaultStyle);
        layer.redraw();
    }
}

function setSettlementsLabels(value){
    settlements.display( value );
}

function changeBaseLayer(value){
    map.setBaseLayer(base_layers[value]);
}
