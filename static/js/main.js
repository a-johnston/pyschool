$(document).ready(function () {
  $.djangocsrf( "enable" );

  var output = $('#output-box');

  var outf = function (text) {
    output.text(output.text() + text);
  };

  $("#clear-output").click(function () {
    output.text("");
  });

  $("#run-code").click(function () {
    runCode(cm);
  });

  $("#input-toggle").click(togglePaneSize);

  function builtinRead(x) {
    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
      throw "File not found: '" + x + "'";
    return Sk.builtinFiles["files"][x];
  }

  function runCode(editor) {
    console.log(editor);
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
    "Shift-Tab"  : togglePaneSize
  };

  var cm = CodeMirror.fromTextArea($("#cm-ta")[0], {
    mode: "python",
    theme: "monokai",
    lineNumbers: true,
    textWrapping: false,
    indentUnit: 4,
    extraKeys: keymap,
    parserConfig: {'pythonVersion': 2, 'strictErrors': true},
  });
});
