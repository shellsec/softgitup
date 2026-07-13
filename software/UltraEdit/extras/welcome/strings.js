/*

"langs" - the object holding all items that need localizations

In order for translations to work, the string in HTML source
should be encapsulated in a <span> with a class set to "l_"
PLUS the unique name of the sub-object containing its
translations.

For example, to translate "Install all" in HTML source, find
(or add) that sub-item in the langs object.  It already
exists with a name of "installAll".  Therefore the <span>
surrounding the text in the HTML source should be assigned a
class of "l_installAll". Example:

    <span class="l_installAll">Install all</span>

It's easy enough to add new translated strings.  Simply copy
one of the existing below, give it a unique name, and enter
the translated strings.  Then add the "l_" + unique name
class to a <span> around the original string in the HTML
source.

var "lng" controls which localization is used.

en = English
ptb - Portuguese (Brazilian)
de = German
fr = French
sp = Spanish
it = Italian
ko = Korean
ja = Japanese
chs = Chinese (Simplified)
cht = Chinese (Traditional)

*/

var lng = 'en';

langs = {

  header : {
    en: '4 quick clicks to make <span id="productName"></span> yours.',
    ptb:'4 cliques rápidos para que o <span id="productName"></span> seja seu.',
    de: 'Nur 4 Klicks und schon gehört <span id="productName"></span> Ihnen.',
    fr: '4 clics rapides pour que <span id="productName"></span> soit à vous.',
    sp: 'Cuatro rápidos clics para personalizar <span id="productName"></span>.',
    it: 'Bastano 4 semplici clic perché <span id="productName"></span> sia tuo.',
    ko: '<span id="productName"></span>을(를) 받으려면 빠르게 4번 클릭하십시오.',
    ja: '4度素早くクリックするだけで<span id="productName"></span>オリジナルが作れます。',
    chs:'快速点击 4 次即可让 <span id="productName"></span> 为您所用。',
    cht:'只要點按 4 次，<span id="productName"></span>就是您的。'
  },

  theme_head : {
    en: '1 | Theme',
    ptb: '1 | Tema',
    de: '1 | Thema',
    fr: '1 | Thème',
    sp: '1 | Tema',
    it: '1 | Tema',
    ko: '1 | 테마',
    ja: '1 | テーマの',
    chs: '1 | 主题',
    cht: '1 | 主題'
  },

  theme_caption : {
    en: 'Switch themes under Layout &raquo; Themes.',
    ptb:'Troque temas em Layout &raquo; Temas.',
    de: 'Themen ändern Sie unter Layout &raquo; Themen.',
    fr: 'Changez de thème sous Disposition&raquo; Thèmes.',
    sp: 'Cambie los temas en Diseño &raquo; Temas.',
    it: 'Cambia tema nella scheda Layout & Tema',
    ko: '레이아웃 &raquo; 테마에서 테마를 전환하십시오.',
    ja: 'レイアウト&raquo; テーマの下でテーマを切り替えましょう。',
    chs:'在“布局”&raquo;“主题”下可切换主题。',
    cht:'在配置 &raquo; 主題下切換主題。'
  },

  layout_head : {
    en: '2 | Layout',
    ptb: '2 | Layout',
    de: '2 | Layout',
    fr: '2 | Disposition',
    sp: '2 | Diseño',
    it: '2 | Layout',
    ko: '2 | 레이아웃',
    ja: '2 | レイアウト',
    chs: '2 | 布局',
    cht: '2 | 版面配置'
  },

  layout_caption : {
    en: 'Create custom layouts under Layout &raquo; Layouts.',
    ptb:'Crie layouts personalizados em Layout &raquo; Layouts.',
    de: 'Benutzerdefinierte Layouts können Sie unter Layout &raquo; Layout erstellen.',
    fr: 'Créez des dispositions personnalisées sous Disposition&raquo; Dispositions',
    sp: 'Cree diseños personalizados en Diseño &raquo; Diseños.',
    it: 'Crea layout personalizzati nella scheda Layout & Layout',
    ko: '레이아웃 &raquo; 레이아웃에서 사용자 지정 레이아웃을 생성하십시오.',
    ja: 'レイアウト &raquo; レイアウトの下でカスタムレイアウトを作成しましょう。',
    chs:'在“布局”&raquo;“布局”下可创建自定义布局。',
    cht:'在配置 &raquo; 配置下建立自訂配置。'
  },

  layout_balanced : {
    en: 'Balanced',
    ptb: 'Equilibrado',
    de: 'Ausgewogen',
    fr: 'Équilibré',
    sp: 'Balanced',
    it: 'Balanced',
    ko: 'Balanced',
    ja: 'Balanced',
    chs: '平衡',
    cht: '平衡'
  },

  layout_lean : {
    en: 'Lean',
    ptb: 'Elegante',
    de: 'Kompakt',
    fr: 'Minimaliste',
    sp: 'Lean',
    it: 'Lean',
    ko: 'Lean',
    ja: 'Lean',
    chs: '精简',
    cht: '精簡'
  },

  layout_clean : {
    en: 'Clean',
    ptb: 'Limpo',
    de: 'Sauber',
    fr: 'Net',
    sp: 'Clean',
    it: 'Clean',
    ko: '지우기',
    ja: 'Clean',
    chs: '简洁',
    cht: '簡潔'
  },

  layout_multi : {
    en: 'Multi-window',
    ptb: 'Multijanela',
    de: 'Mehrfenster',
    fr: 'Multi-fenêtre',
    sp: 'Multi-window',
    it: 'Multi-window',
    ko: 'Multi-window',
    ja: 'Multi-window',
    chs: '多窗口',
    cht: '多視窗'
  },

  ribbon_head : {
    en: '3 | Ribbon or menu / toolbars',
    ptb:'3 | Faixa de opções ou menu / ferramentas',
    de: '3 | Menüband oder Menü / Symbolleisten',
    fr: '3 | Ruban ou menu / barre d’outils',
    sp: '3 | Cinta o menú/barras de herramientas',
    it: '3 | Ribbon o menu / barre degli strumenti',
    ko: '3 | 리본 또는 메뉴 / 도구 모음',
    ja: '3 | リボンもしくはメニュー / ツールバー',
    chs:'3 | 功能区或菜单/工具栏',
    cht:'3 | Ribbon 或功能表/工具列'
  },

  ribbon_caption : {
    en: 'Switch between them later by right-clicking on the ribbon or menu.',
    ptb:'Alterne entre eles mais tarde clicando com o botão direito do mouse na faixa de opções ou no menu.',
    de: 'Durch einen Klick mit der rechten Maustaste auf das Menüband oder das Menü können Sie später zwischen den Anzeigen wechseln.',
    fr: 'Basculez entre les options ultérieurement en cliquant sur le ruban ou le menu.',
    sp: 'Alterne entre ellas después haciendo clic con el botón derecho en la cinta o menú.',
    it: 'Passa da uno all\'altro più tardi cliccando con il tasto destro del mouse sul ribbon o sul menu.',
    ko: '리본 또는 메뉴를 마우스 오른쪽 버튼으로 클릭해서 나중에 전환할 수 있습니다.',
    ja: 'リボンもしくはメニューで右クリックすると後で切り替えられます。',
    chs:'稍后可通过右键单击功能区或菜单在它们之间切换。',
    cht:'在 ribbon 或功能表上按一下右鍵，以便在稍後進行切換。'
  },

  ribbon : {
    en: 'Ribbon',
    ptb: 'Faixa de opções',
    de: 'Menüband',
    fr: 'Ruban',
    sp: 'Cinta',
    it: 'Barra multifunzione',
    ko: '리본',
    ja: 'リボン',
    chs: 'Ribbon',
    cht: 'Ribbon'
  },

  menus : {
    en: 'Menu / toolbars',
    ptb: 'Menu / barras de ferramentas',
    de: 'Menü / Symbolleisten',
    fr: 'Menu / barres d\'outils',
    sp: 'Menú / barras de herramientas',
    it: 'Menu / barre strumenti',
    ko: '메뉴 / 도구바',
    ja: 'メニュー / ツールバー',
    chs: '菜单 / 工具栏',
    cht: '功能表 / 工具列'
  },

  menu_only : {
    en: 'Menu only',
    ptb:'Menu apenas',
    de: 'Nur Menü',
    fr: 'Menu uniquement',
    sp: 'Solo menú',
    it: 'Solo menu',
    ko: '메뉴만',
    ja: 'メニューのみ',
    chs:'仅限菜单',
    cht:'僅限功能表'
  },

  settings_head : {
    en: '4 | A couple settings',
    ptb:'4 | Algumas configurações',
    de: '4 | Einige Einstellungen',
    fr: '4 | Quelques paramètres',
    sp: '4 | Un par de ajustes',
    it: '4 | Un paio di impostazioni',
    ko: '4 | 연결 설정',
    ja: '4 | 複数の設定',
    chs:'4 | 配对设置',
    cht:'4 | 幾種設定'
  },

  backups : {
    en: 'Backups',
    ptb: 'Backups',
    de: 'Sicherheitskopien',
    fr: 'Sauvegardes',
    sp: 'Salvados',
    it: 'Sicurezza',
    ko: '백업',
    ja: 'バックアップ',
    chs: '备份',
    cht: '備份'
  },

  backup_option_1 : {
    en: 'Create .bak files where original file is saved',
    ptb:'Criar arquivos .bak onde o arquivo original foi salvo',
    de: '.bak Dateien im Ordner der Originaldatei erstellen',
    fr: 'Créez des fichiers .bak à l\'emplacement d\'enregistrement du fichier d\'origine',
    sp: 'Crear archivos .bak donde se guarda el archivo original',
    it: 'Crea file .bak nella location dove sono salvati i file originali',
    ko: '원본 파일이 저장되는 .bak 파일 생성',
    ja: 'オリジナルファイルを保存した場所で.bakファイルを作成',
    chs:'在保存原始文件的位置创建 .bak 文件',
    cht:'在儲存原始檔案的地方建立 .bak 檔案'
 },

  backup_option_2 : {
    en: 'Create .bak files in this folder:',
    ptb:'Criar arquivos .bak nesta pasta:',
    de: '.bak Dateien in diesem Ordner erstellen:',
    fr: 'Créez des fichiers .bak dans ce dossier :',
    sp: 'Crear archivos .bak en esta carpeta:',
    it: 'Crea file .bak in questa cartella:',
    ko: '이 폴더에 .bak 파일 생성:',
    ja: 'このフォルダで.bakファイルを作成:',
    chs:'在此文件夹中创建 .bak 文件：',
    cht:'在此資料夾建立 .bak 檔案：'
  },

  backup_option_3 : {
    en: 'Do not create backups',
    ptb:'Não criar backups',
    de: 'Keine Sicherungsdateien erstellen',
    fr: 'Ne créez pas de sauvegardes',
    sp: 'No crear copias de seguridad',
    it: 'Non creare copie di backup',
    ko: '백업 생성 안 함',
    ja: 'バックアップを作成しないでください',
    chs:'不创建备份',
    cht:'不要建立備份'
  },

  tabs : {
    en: 'Tabs',
    ptb: 'Tabulações',
    de: 'Tabulatoren',
    fr: 'Tabulations',
    sp: 'Tabulaciones',
    it: 'Tabulazioni',
    ko: '탭',
    ja: 'タブ',
    chs: '制表符',
    cht: '製表符'
  },

  tabs_option_1 : {
    en: 'Indent size:',
    ptb:'Tamanho do recuo:',
    de: 'Einzugsgröße:',
    fr: 'Taille du retrait :',
    sp: 'Tamaño de sangría:',
    it: 'Dimensione rientri:',
    ko: '들여쓰기 크기:',
    ja: 'インデントサイズ:',
    chs:'缩进尺寸：',
    cht:'縮排尺寸：'
  },

  tabs_option_2 : {
    en: 'Insert a tab',
    ptb:'Inserir uma guia',
    de: 'Tabulator einfügen',
    fr: 'Insérer une tabulation',
    sp: 'Insertar un tabulador',
    it: 'Inserisci una scheda',
    ko: '탭 삽입',
    ja: 'タブを挿入',
    chs:'插入制表符',
    cht:'插入定位點'
  },

  tabs_option_3 : {
    en: 'Insert spaces',
    ptb:'Inserir espaços',
    de: 'Leerzeichen einfügen',
    fr: 'Insérer des espaces',
    sp: 'Insertar espacios',
    it: 'Inserisci spazi',
    ko: '공백 삽입',
    ja: '空白を挿入',
    chs:'插入空格',
    cht:'插入空格'
  },


}
