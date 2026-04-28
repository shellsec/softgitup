window.onload = function () { window.location.href = '#ONLOADCOMPLETE'; };

var collapsedNodes = [];

function idmBrowser_notify(id, param) {
  try {
    var data;
    try {
      if (param)
        data = param;
    } catch (error) { data = null; }
    var notifyData = id;
    if (data)
      notifyData += "|" + data;
    try {
      window.external.notify(notifyData);
    } catch (error) {
      window.location.href = "#" + notifyData;
    }
  } catch (error) {
    return;
  }
}

function toggleNode(node, init) {
  try {
    var nodeElem = document.getElementById(node);
    var ctrlElem = document.getElementById(node + '_toggler');
    if (ctrlElem) {
      var ctrlElemChilds = ctrlElem.childNodes;
      if (init) {
        ctrlElemChilds[0].classList.add('notransition');
      } else {
        ctrlElemChilds[0].classList.remove('notransition');
      }
      if (nodeElem.style.display === 'none') { // node was collapsed, is expanding
        nodeElem.style.display = 'block';
        ctrlElem.classList.remove('fp_node_hidden');
        // Remove from collapsed array obj
        var nIdx = collapsedNodes.indexOf(node);
        if (nIdx > -1) {
          collapsedNodes.splice(nIdx, 1);
        }
        if (!init) {
          idmBrowser_notify('FP_NOTIFY_EXPAND', node);
        }
      } else { // node was expanded, is collapsing
        nodeElem.style.display = 'none';
        ctrlElem.classList.add('fp_node_hidden');
        // Add to obj
        collapsedNodes.push(node);
        if (!init) {
          idmBrowser_notify('FP_NOTIFY_COLLAPSE', node);
        }
      }
    }
  } catch (error) {
    return;
  }
}

function idmBrowser_collectCollapsedNodes() {
  try {
    var returnStr = '';
    if (collapsedNodes.length > 0) {
      for (var i = 0; i < collapsedNodes.length; i++) {
        if (i > 0) {
          returnStr += ',';
        }
        returnStr += collapsedNodes[i];
      }
    }
    return returnStr;
  } catch (error) {
    return "";
  }
}

function idmBrowser_loadCollapsedNodes(param) {
  try {
    var json = JSON.parse(param);
    var nodes = json.nodes;
    if (typeof nodes === 'string') {
      nodesToCollapse = nodes.split(',');
      for (var i = 0; i < nodesToCollapse.length; i++) {
        toggleNode(nodesToCollapse[i], true);
      }
    }
  } catch (error) {
    return;
  }
}

function idmBrowser_localize(param) {
  try {
    var json = JSON.parse(param);
    var lang = json.language;
    if (!lang || loc_supportedLangs.indexOf(lang) == -1) {
      lang = 'en';
    }

    for (var str in loc_langs) {
      var uid = 'l_' + str;
      var els = document.querySelectorAll('.' + uid);
      for (var i = 0; i < els.length; i++) {
        els[i].innerHTML = loc_langs[str][lang];
      }
    }
  } catch (error) {
    return;
  }
}

function idmBrowser_eval(param) {
  try {
    return eval(param);
  } catch (error) {
    return;
  }
}

