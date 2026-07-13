window.onload = function() {

  // UE or UES?
  var product  = getParam('prod') ? getParam('prod') : 'ue';
  var language = getParam('ln') ? getParam('ln') : 'en';
  var theme    = getParam('theme') ? getParam('theme') : '';
  var layout   = getParam('layout') ? getParam('layout') : '';
  var mode     = getParam('mode') ? getParam('mode') : '';
  var backup   = getParam('backup') ? getParam('backup') : '';
  var backupDir= getParam('backupdir') ? getParam('backupdir') : '';
  var tabs     = getParam('tabs') ? getParam('tabs') : '';
  var tabSize  = getParam('tabsize') ? getParam('tabsize') : '';

  /* ----------------------------------
      1) Localize + set product name
  ------------------------------------- */
  // Localize strings
  for (var str in langs) {
    var uid = 'l_' + str;
    var elems = document.querySelectorAll('.' + uid);

    for (var i = 0; i < elems.length; i++) {
      elems[i].innerHTML = langs[str][language];
    }
  }

  // Localize images
  var img_elems = document.querySelectorAll('.img_loc');
  for (var i = 0; i < img_elems.length; i++) {
    if (language !== 'en') {
      img_elems[i].src = img_elems[i].src.replace(/(\/[\w\d\s\-\_]+\.\w+$)/gi, '/' + language + '/' + "$1");
    }
  }

  // Set application name
  var productName = document.getElementById('productName');
  productName.innerHTML = conf_apps[product].appname;

  // Set default layout selection based on the app
  var layouts = ['Balanced', 'Lean', 'Clean', 'Multi-Window'];
  if (layout !== '') {
    for (i = 0; i < layouts.length; i++) {
      var element = document.getElementById(layouts[i]);
      if (element) {
        var cClass = element.className.replace("chosen", "");
        element.setAttribute('class', layout === layouts[i] ? cClass + ' chosen' : cClass);
      }
    }
  }

  // Set default theme selection based on the app
  var themes = ['theme_1_click', 'theme_2_click', 'theme_3_click', 'theme_4_click', 'theme_5_click'];
  if (theme !== '') {
    for (i = 0; i < themes.length; i++) {
      var element = document.getElementById(themes[i]);
      if (element) {
        element.className = element.className.replace("chosen", "");
        if (theme === themes[i]) {
          element.className += ' chosen';
          var DynCssAttr = element.getAttribute('data-css');
          if (DynCssAttr) {
            removeElement(element);
            var head = document.getElementsByTagName('head')[0];
            var s = document.createElement('link');
            s.setAttribute('rel', 'stylesheet');
            s.setAttribute('href', element.getAttribute('data-css') + '.css');
            s.setAttribute('id', 'CssDynAdd');
            head.appendChild(s);
          }
          //var element2 = document.getElementById('theme_1_click');
          //element2.className = element2.className.replace("chosen", "");
        }
      }
    }
  }

  // Set default mode selection based on the app
  var modes = ['ribbon', 'menus_toolbars', 'menus'];
  if (mode !== '') {
    for (i = 0; i < modes.length; i++) {
      var element = document.getElementById(modes[i]);
      if (element) {
        var cClass = element.className.replace("chosen", "");
        element.className = mode === modes[i] ? cClass + ' chosen' : cClass;
      }
    }
  }

  // Set settings based on the app
  if (tabs !== '') {
    var element = document.getElementById('s_tab_' + tabs);
    if (element) {
      element.checked = true;
    }
  }

  if (tabSize !== '') {
    var element = document.getElementById('s_tab_size');
    if (element) {
      element.value = tabSize;
    }
  }

  if (backup !== '') {
    var element = document.getElementById('s_bak_' + backup);
    if (element) {
      element.checked = true;
    }
  }

  if (backupDir !== '') {
    var element = document.getElementById('s_bak_2i');
    if (element) {
      element.value = backupDir;
    }
  }

  /* ----------------------------------
      2) Set up listeners for selector classes
  ------------------------------------- */

  // selectThings should contain all IDs of tables containing a user-selectable setting
  var selectThings = ["layout_select", "ribbon_select"];
  var classChoice = "select";
  var classAdd = "chosen";

  for (i = 0; i < selectThings.length; i++) {
    setUpListener(selectThings[i]);
  }

  function setUpListener(elemID) {
    var t = document.getElementById(elemID);
    var selectors = t.getElementsByClassName(classChoice);
    for (var i = 0; i < selectors.length; i++) {
      selectors[i].addEventListener('click', function() {
        var regex = new RegExp("(?:^|\\s)" + classAdd + "(?!\\S)", "g");
        for (var i = 0; i < selectors.length; i++) {
          selectors[i].className = selectors[i].className.replace(regex, '');
        }
        // now add it to clicked element - remember IE doesn't support event.target
        var evt = event.target || window.event.srcElement;
        evt.parentElement.className += " " + classAdd;
      });
    }
  }

  // Set up listener for on-the-fly CSS / theme switch
  var themeEls = document.getElementsByClassName('selectTheme');
  for (i = 0; i < themeEls.length; i++) {
    var cssAttr = themeEls[i].getAttribute('data-css');
    if (cssAttr) {
      var addCSS = cssAttr + ".css"
      themeEls[i].addEventListener('click', function() {
        for (i = 0; i < themes.length; i++) {
          var element = document.getElementById(themes[i]);
          if (element) {
            element.className = element.className.replace("chosen", "");
          }
        }
        var evt = event.target || window.event.srcElement;
        evt.parentElement.className += " " + classAdd;
        removeElement('CssDynAdd')
        var head = document.getElementsByTagName('head')[0];
        var s = document.createElement('link');
        s.setAttribute('rel', 'stylesheet');
        s.setAttribute('href', this.getAttribute('data-css') + '.css');
        s.setAttribute('id', 'CssDynAdd');
        head.appendChild(s);
      });
    } else {
      // in this case, default style should be used,
      // so we must REMOVE any dynamically inserted style
      themeEls[i].addEventListener('click', function() {
        for (i = 0; i < themes.length; i++) {
          var element = document.getElementById(themes[i]);
          if (element) {
            element.className = element.className.replace("chosen", "");
          }
        }
        var evt = event.target || window.event.srcElement;
        evt.parentElement.className += " " + classAdd;
  		  removeElement('CssDynAdd')
      });
    }
  }

  /* -------- funcs -------------------- */

  // Adds CSS to end of <head>
  function removeElement(element) {
    var element = document.getElementById('CssDynAdd');
    if (element) element.parentNode.removeChild(element);
  }


  // Gets URL parameters
  function getParam(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null
  }

  InitNativeHandlers();

  window.location.href = "#ONLOADCOMPLETE";
};

function SetupNativeHandlers(Ids, type) {
  for (i = 0; i < Ids.length; i++) {
    var element = document.getElementById(Ids[i]);
    element.addEventListener(type, function (event) {
      var id = event.target.id;
      var params = {
        id: id,
        type: type,
        data: event.target.value
      };
      sendToNative(id, params);
    });
  }
}

function InitNativeHandlers() {
  //Theme handlers
  var themeIds = ["theme_1_click", "theme_2_click", "theme_3_click", "theme_4_click", "theme_5_click"];
  SetupNativeHandlers(themeIds, 'click');

  //Layout handlers
  var layoutIds = ["Balanced", "Lean", "Clean", "Multi-Window"];
  SetupNativeHandlers(layoutIds, 'click');

  //Ribbon mode handlers
  var ribbonIds = ["ribbon", "menus_toolbars", "menus"];
  SetupNativeHandlers(ribbonIds, 'click');

  //Backup/Tab handlers
  var backupTabClickIds = ["s_bak_1", "s_bak_2", "s_bak_3", "s_tab_1", "s_tab_2", "s_bak_bff"];
  SetupNativeHandlers(backupTabClickIds, 'click');
  var backupTabChangeIds = ["s_bak_2i", "s_tab_size"];
  SetupNativeHandlers(backupTabChangeIds, 'change');
}

function sendToNative(command, params) {
  var message = {
    message: command,
    args: params
  };
  try {
    window.chrome.webview.postMessage(message);
  } catch (error) {
    console.log("WebView2 unavailable, cannot send message to native application: " + JSON.stringify(message));
    window.location.href = "#UE_BROWSER_MSG#" + JSON.stringify(message);
  }
}

function external_eval(param) {
  try {
    return eval(param);
  } catch (error) {
    return;
  }
}

// Object with app names and properties
conf_apps = {

  ue: {
    appname: 'UltraEdit'
  },

  ues: {
    appname: 'UEStudio'
  },

  uep: {
    appname: 'UE Mobile'
  },

  uc: {
    appname: 'UltraCompare'
  },

  uf: {
    appname: 'UltraFinder'
  },

  us: {
    appname: 'UltraSentry'
  },

  ucp: {
    appname: 'UC Mobile'
  }
};
