var urlRegExp =/^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?$/i;

function handle_enable_disable(){
    if ($("#enable-tracking").prop("checked")){
        $("#url").attr("disabled", false);
    }
    else{
        $("#url").attr("disabled", true);
    }
}

function getQueryParam(variable, default_) {
    var query = location.search.substring(1);
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (pair[0] == variable){
            return decodeURIComponent(pair[1]);
        }
    }
    return default_ || false;
}

function save(){
    if (urlRegExp.test($("#url").val())){
        localStorage.setItem("url", $("#url").val());
        localStorage.setItem("enable", $("#enable-tracking").prop("checked"));
        var return_to = getQueryParam('return_to', 'pebblejs://close#');
        document.location = return_to +
            encodeURIComponent(JSON.stringify({
                url: $("#url").val(),
                enabled: $("#enable-tracking").prop("checked")
            }));
    } else {
        $("#url").addClass("bad").removeClass("good");
    }
}

function load(){
    var url = localStorage.getItem("url");
    var enable = localStorage.getItem("enable");
    enable = enable === "true" ? true : false;
    if (url !== null) {
        $("#url").val(url);
        $("#enable-tracking").prop("checked", enable);
    }
    else {
        $("#url").val("");
        $("#enable-tracking").prop("checked", true);
    }

    handle_enable_disable();

    $("#enable-tracking").change(function(){
        handle_enable_disable();
    });

    $("#save-url").click(function(){
        save();
    });

    $("#url").focus(function(){
        $("#url").addClass("good").removeClass("bad");
    });
}
