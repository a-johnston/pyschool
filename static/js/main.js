var regMode = false;

var selectedChallenge = null;
var completedCallback = null;

var cm = null;

var outf = null;
var rawOutf = null;

$(document).ready(function () {
  $.djangocsrf( "enable" );

  var output = $('#output-box');

  outf = function (text) {
    output.html(output.html() + text.replace("<", "&lt;").replace("&", "&amp;"));
  };

  rawOutf = function (text) {
    output.html(output.html() + text);
  };

  $("#clear-output").click(function () {
    output.text("");
  });

  $("#run-code").click(function () {
    runCode(cm);
  });

  $("#input-toggle").click(togglePaneSize);

  $("#ch-button").click(function () {
    $("#challenges").toggleClass("open-challenges");
  });

  $("#login-button").click(function () {
    if (regMode) {
        toggleReg();

        if (!$("#login-container").hasClass("big-title")) {
            $("#login-container").toggleClass("big-title");
        }
    } else {
        $("#login-container").toggleClass("big-title");
    }
  });

  $("#register-button").click(function () {
    if (!regMode) {
        toggleReg();

        if (!$("#login-container").hasClass("big-title")) {
            $("#login-container").toggleClass("big-title");
        }
    } else {
        $("#login-container").toggleClass("big-title");
    }
  });

  $(".reg-button").click(toggleReg);

  function toggleReg() {
    regMode = !regMode;
    $("#reg-div").toggleClass("reg-div-big");
    $("#login-container p").toggleClass("login-alt-text");
  }

  function builtinRead(x) {
    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
      throw "File not found: '" + x + "'";
    return Sk.builtinFiles["files"][x];
  }

  function runCode(editor) {
    Sk.configure({output: outf, read: builtinRead});
    Sk.pre = "output-box";
    try {
      Sk.misceval.asyncToPromise(function() {
        try {
          return Sk.importMainWithBody("<stdin>",false,editor.getValue() + ' ',true);
        } catch(e) {
          outf(e.toString() + "\n");
        }
      });
    } catch(e) {
      outf(e.toString() + "\n");
    }
  }

  function togglePaneSize() {
    $("#output-container").toggleClass("text-mini");
    $("#input-container").toggleClass("text-mini");
  }

  var keymap = {
    "Ctrl-Enter" : runCode,
    "Shift-Tab"  : togglePaneSize,
    "Shift-Ctrl-Enter": handleChallenge
  };

  cm = CodeMirror.fromTextArea($("#cm-ta")[0], {
    mode: "python",
    theme: "monokai",
    lineNumbers: true,
    textWrapping: false,
    indentUnit: 4,
    extraKeys: keymap,
    parserConfig: {'pythonVersion': 2, 'strictErrors': true},
  });

  cm.on("changes", function () {
    $.cookie("code", cm.doc.getValue(), { path: '/', expires: 10 });
  });

  var oldCode = $.cookie("code");

  if (oldCode) {
    cm.doc.setValue(oldCode)
  }
});

function handleAccount(form) {
    values = {'username': form.elements[0].value,
              'password': form.elements[1].value };
    if (regMode) {
        jQuery.post("/register/", values, accountCallback);
    } else {
        jQuery.post("/login/", values, accountCallback);
    }
}

function printcolor(text, color) {
    rawOutf("<div style='color:" + color + "'>" + text + "</div>");
}

function handleChallenge() {
    if (selectedChallenge == null) {
        return;
    }
    printcolor("Submitting code...", "#66d9ef"); 
    values = {'name': selectedChallenge,
              'code': cm.getValue() };

    jQuery.post("/submit/", values, submitCallback);
}

function accountCallback(obj, stat, x) {
    window.location = "/";
}

function submitCallback(data) {
    if (data == 'failed') {
        printcolor("Challenge incomplete! :(", "red");
    } else if (data == 'success') {
        printcolor("Challenge completed!", "greenyellow");
        if (completedCallback) {
            completedCallback();
        }
    } else {
        printcolor("Level completed!");
        if (completedCallback) {
            completedCallback();
        }
        
        window.location = "/"; //jaaank
    }
}

function selectChallenge(option, name, desc) {
    $("#challenges a").removeClass("selected");
    if (name != selectedChallenge) {
        $(option).addClass("selected");
        $("#challenge-detail").addClass("detail-view");
        selectedChallenge = name;

        $("#challenge-detail #ch-title").text(name);
        $("#challenge-detail #ch-desc").text(desc);

        completedCallback = function () {
            $(option).append("<p class='done'>Done!</p>");
        };
    } else {
        selectedChallenge = null;
        completedCallback = null;
        $("#challenge-detail").removeClass("detail-view");
    }
}
