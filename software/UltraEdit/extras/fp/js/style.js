idmBrowser_UpdateTheme();

function idmBrowser_UpdateTheme(jsonTheme) {
  try {
    var theme = jsonTheme ? JSON.parse(jsonTheme) : null;

    var c_fg = theme ? "#" + theme.fg : '#ffffff';
    var c_bg = theme ? "#" + theme.bg : '#4b4b4b';
    var c_hl = theme ? "#" + theme.hl : '#0088ca';

    var c_hla = LightenDarkenColor(c_hl, 10);
    var c_fgs = LightenDarkenColor(c_fg, -35);
    var c_fgl = LightenDarkenColor(c_fg, -20);
    var c_bgd = LightenDarkenColor(c_bg, -35);

    var sheet = document.createElement('style');

    var d_styles = 'body { color: ' + c_fg + '; background-color: ' + c_bg + '} ';
    d_styles += 'a:link,a:visited,a:hover,a:active { color: ' + c_fg + '; } ';
    d_styles += '.fp_table tr td.fp_value { font-weight: 600; } ';
    d_styles += '.fp_table tr td.fp_label a, a.fp_toggle:hover, a.fp_toggle:active { color: ' + c_fgs + '; } ';
    d_styles += '.fp_title { color: ' + c_fgs + '; } ';
    d_styles += '.fp_copy_svg, .fp_toggle_svg { fill: ' + c_fgs + '; } ';
    d_styles += 'a#fp_btn_refresh .fp_refresh_svg { fill: ' + c_fgs + '; } ';
    d_styles += 'a#fp_btn_refresh:hover .fp_refresh_svg, a#fp_btn_refresh:active .fp_refresh_svg { fill: ' + c_fg + '; } ';
    d_styles += '#fp_footer { background-color: ' + c_bg + '} ';
    d_styles += '#fp_footer a:link, #fp_footer a:visited { color: red; }';
    d_styles += '#fp_footer a { color: ' + c_fgs + '; text-decoration: underline;} ';
    d_styles += '#fp_footer a:hover, #fp_footer :active { color: ' + c_fg + '; } ';
    d_styles += '#fp_footer a:hover .fp_copy_svg, #fp_footer a:active .fp_copy_svg { fill: ' + c_fg + '; } ';

    sheet.innerHTML = d_styles;
    if (theme) {
      document.head.replaceChild(sheet, document.head.lastChild);
    } else {
      document.head.appendChild(sheet);
    }
  } catch (error) {
    return;
  }
}

function LightenDarkenColor(color, percent) {
  try {
    var R = parseInt(color.substring(1, 3), 16);
    var G = parseInt(color.substring(3, 5), 16);
    var B = parseInt(color.substring(5, 7), 16);

    R = parseInt(R * (100 + percent) / 100);
    G = parseInt(G * (100 + percent) / 100);
    B = parseInt(B * (100 + percent) / 100);

    R = (R < 255) ? R : 255;
    G = (G < 255) ? G : 255;
    B = (B < 255) ? B : 255;

    var RR = ((R.toString(16).length == 1) ? "0" + R.toString(16) : R.toString(16));
    var GG = ((G.toString(16).length == 1) ? "0" + G.toString(16) : G.toString(16));
    var BB = ((B.toString(16).length == 1) ? "0" + B.toString(16) : B.toString(16));

    return "#" + RR + GG + BB;
  } catch (error) {
    return "";
  }
}
