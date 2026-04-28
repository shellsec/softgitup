function hereDoc(f) {
  try {
    return f.toString().
      replace(/^[^\/]+\/\*!?/, '').
      replace(/\*\/[^\/]+$/, '');
  } catch (error) {
    return;
  }
}

function getParam(name) {
  try {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search) || [, ""])[1].replace(/\+/g, '%20')) || null
  } catch (error) {
    return "";
  }
}

function replaceInnerHTML(replaceID, replaceWith) {
  try {
    var e = document.getElementById(replaceID);
    if (e) e.innerHTML = replaceWith;
  } catch (error) {
    return;
  }
}

loc_supportedLangs = [
  "en",
  "ptb",
  "de",
  "fr",
  "es",
  "it",
  "ko",
  "jp",
  "ch",
  "cht"
];

loc_langs = {

  hdr_information: {
    en: 'Information',
    ptb: 'Informações',
    de: 'Informationen',
    fr: 'Informations',
    es: 'Información',
    it: 'Informazioni',
    ko: '정보',
    jp: '情報のご案内',
    ch: '信息',
    cht: '信息'
  },

  hdr_contents: {
    en: 'Contents',
    ptb: 'Conteúdo',
    de: 'Inhalte',
    fr: 'Contenus',
    es: 'Contenido',
    it: 'Contenuti',
    ko: '콘텐츠',
    jp: 'コンテンツ',
    ch: '内容',
    cht: '內容'
  },

  hdr_statistics: {
    en: 'Statistics',
    ptb: 'Estatísticas',
    de: 'Zeicheneigenschaften',
    fr: 'Statistiques',
    es: 'Estadísticas',
    it: 'Statistiche',
    ko: '통계',
    jp: '統計値',
    ch: '统计数据',
    cht: '統計資料'
  },

  fp_path: {
    en: 'Path:',
    ptb: 'Caminho:',
    de: 'Pfad',
    fr: 'Chemin',
    es: 'Ruta',
    it: 'Percorso',
    ko: '경로',
    jp: 'パス',
    ch: '路径',
    cht: '路徑'
  },

  fp_opens_with: {
    en: 'Opens with:',
    ptb: 'Abrir com:',
    de: 'Öffnet mit:',
    fr: 'S’ouvre avec :',
    es: 'Abre con:',
    it: 'Si apre con:',
    ko: '다음과 함께 시작:',
    jp: '次で開く:',
    ch: '打开方式：',
    cht: '開啟程式：'
  },

  fp_size_original: {
    en: 'Size (saved):',
    ptb: 'Tamanho (salvo):',
    de: 'Größe (gespeichert):',
    fr: 'Taille (enregistré) :',
    es: 'Tamaño (guardado):',
    it: 'Dimensioni (salvato):',
    ko: '크기 (저장) :',
    jp: 'サイズ（保存）:',
    ch: '尺寸（已保存）：',
    cht: '尺寸（已儲存）：'
  },

  fp_size_current: {
    en: 'Size (current):',
    ptb: 'Tamanho (atual):',
    de: 'Größe (aktuell):',
    fr: 'Taille (actuelle) :',
    es: 'Tamaño (actual):',
    it: 'Dimensioni (attuali):',
    ko: '크기(현재):',
    jp: 'サイズ（現在）：',
    ch: '尺寸（当前）：',
    cht: '尺寸(目前)：'
  },

  fp_date_created: {
    en: 'Date created:',
    ptb: 'Data de criação:',
    de: 'Erstellungsdatum:',
    fr: 'Date de création :',
    es: 'Fecha Creación:',
    it: 'Data di Creazione:',
    ko: '만든 날짜:',
    jp: '作成日時:',
    ch: '创建日期:',
    cht: '創建日期:'
  },

  fp_date_modified: {
    en: 'Date modified:',
    ptb: 'Data de modificação:',
    de: 'Änderungsdatum:',
    fr: 'Date modifiée :',
    es: 'Fecha de modificación:',
    it: 'Data ultima modifica:',
    ko: '수정한 날짜:',
    jp: '変更日付:',
    ch: '修改日期:',
    cht: '修改日期:'
  },

  fp_date_accessed: {
    en: 'Date accessed:',
    ptb: 'Data de acesso:',
    de: 'Zugriffsdatum:',
    fr: 'Site consulté :',
    es: 'Fecha de acceso:',
    it: 'Data dell’ultimo acceso:',
    ko: '액세스 날짜:',
    jp: 'アクセス日：',
    ch: '访问日期：',
    cht: '訪問日期：'
  },

  fp_attributes: {
    en: 'Attributes:',
    ptb: 'Atributos:',
    de: 'Attribute:',
    fr: 'Attributs :',
    es: 'Atributos:',
    it: 'Attributi:',
    ko: '속성:',
    jp: '属性:',
    ch: '属性:',
    cht: '屬性:'
  },

  fp_owner: {
    en: 'Owner:',
    ptb: 'Proprietário:',
    de: 'Besitzer:',
    fr: 'Propriétaire :',
    es: 'Propietario:',
    it: 'Proprietario:',
    ko: '소유자',
    jp: 'オーナー',
    ch: '所有者',
    cht: '擁有者'
  },

  fp_encoding_detected: {
    en: 'Encoding (detected):',
    ptb: 'Codificação (detectada):',
    de: 'Kodierung (erkannt):',
    fr: 'Codage (détecté) :',
    es: 'Codificación (detectada):',
    it: 'Codifica (rivelata):',
    ko: '인코딩(감지됨):',
    jp: '暗号化（検知）：',
    ch: '编码（已删除）：',
    cht: '編碼(已偵測)：'
  },

  fp_encoding_in_use: {
    en: 'Encoding (in use):',
    ptb: 'Codificação (em uso):',
    de: 'Kodierung (in Verwendung):',
    fr: 'Codage (en cours d’utilisation) :',
    es: 'Codificación (en uso):',
    it: 'Codifica (in uso):',
    ko: '인코딩(사용 중):',
    jp: '暗号化（使用中）：',
    ch: '编码（使用中）：',
    cht: '編碼(現用)：'
  },

  fp_bom: {
    en: 'BOM (if applicable):',
    ptb: 'BOM (se aplicável):',
    de: 'BOM (falls zutreffend):',
    fr: 'BOM (si applicable) :',
    es: 'BOM (si aplica):',
    it: 'BOM (ove applicabile):',
    ko: 'BOM(해당될 경우):',
    jp: 'BOM（該当する場合）：',
    ch: 'BOM（如适用）：',
    cht: 'BOM (若可用)：'
  },

  fp_content_type: {
    en: 'Content type:',
    ptb: 'Tipo de conteúdo:',
    de: 'Inhaltstyp:',
    fr: 'Type de contenu :',
    es: 'Tipo de contenido:',
    it: 'Tipo contenuto:',
    ko: '콘텐츠 유형:',
    jp: '現在のタイプ：',
    ch: '内容类型：',
    cht: '內容類型：'
  },

  fp_line_terminators: {
    en: 'Line terminators:',
    ptb: 'Terminadores de linha:',
    de: 'Zeilenendungen:',
    fr: 'Fins de ligne :',
    es: 'Finalización de líneas:',
    it: 'Terminatori di riga',
    ko: '줄 종료:',
    jp: '行末',
    ch: '行终结符',
    cht: '行結束字元'
  },

  fp_syntax_highlighting: {
    en: 'Syntax highlighting:',
    ptb: 'Destaque de sintaxe:',
    de: 'Syntaxhervorhebung:',
    fr: 'Coloration syntaxique :',
    es: 'Resaltado de sintaxis:',
    it: 'Evidenziazione Sintassi:',
    ko: '구문 강조:',
    jp: 'シンタックスハイライト:',
    ch: '语法高亮:',
    cht: '語法突顯:'
  },

  fp_checksums: {
    en: 'Checksums:',
    ptb: 'Checksums:',
    de: 'Prüfsummen:',
    fr: 'Sommes de contrôle :',
    es: 'Cheques:',
    it: 'Checksum:',
    ko: '체크섬 :',
    jp: 'チェックサム:',
    ch: '校验和:',
    cht: '校驗和：'
  },

  fp_calculate: {
    en: 'Calculate...',
    ptb: 'Calcular...',
    de: 'Berechnen...',
    fr: 'Calculer...',
    es: 'Calcula...',
    it: 'Calcolare...',
    ko: '계산하다...',
    jp: '計算して...',
    ch: '计算...',
    cht: '計算...'
  },

  fp_characters: {
    en: 'Characters:',
    ptb: 'Caracteres',
    de: 'Zeichen:',
    fr: 'Caractères :',
    es: 'Caracteres:',
    it: 'Caratteri:',
    ko: '문자:',
    jp: '文字以下:',
    ch: '个字符:',
    cht: '個字元:'
  },

  fp_lines: {
    en: 'Lines:',
    ptb: 'Linhas:',
    de: 'Zeilen:',
    fr: 'Lignes :',
    es: 'Líneas:',
    it: 'Righe:',
    ko: '줄:',
    jp: '行:',
    ch: '行:',
    cht: '列數：'
  },

  fp_non_empty_lines: {
    en: 'Non-empty lines:',
    ptb: 'Linhas não vazias:',
    de: 'Nicht leere Zeilen:',
    fr: 'Lignes remplies :',
    es: 'Líneas no vacías:',
    it: 'Righe non vuote:',
    ko: '비어 있지 않은 줄:',
    jp: '空でない行のマーク：',
    ch: '非空行：',
    cht: '非空白列：'
  },

  fp_sloc: {
    en: 'SLOC:',
    ptb: 'SLOC:',
    de: 'SLOC:',
    fr: 'SLOC :',
    es: 'SLOC:',
    it: 'SLOC:',
    ko: 'SLOC:',
    jp: 'SLOC：',
    ch: 'SLOC:',
    cht: 'SLOC：'
  },

  fp_average_line_length: {
    en: 'Average line length:',
    ptb: 'Comprimento médio da linha:',
    de: 'Durchschn. Zeilenlänge:',
    fr: 'Longueur moyenne de ligne :',
    es: 'Longitud de línea promedio:',
    it: 'Lunghezza riga media:',
    ko: '평균 줄 길이:',
    jp: '行の平均長：',
    ch: '平均行长：',
    cht: '平均列長：'
  },

  fp_longest_line: {
    en: 'Longest line:',
    ptb: 'Linha mais longa:',
    de: 'Längste Zeile:',
    fr: 'Ligne la plus longue :',
    es: 'Línea más larga:',
    it: 'Riga più lunga:',
    ko: '가장 긴 줄:',
    jp: '最長行：',
    ch: '最长行：',
    cht: '最長列：'
  },

  fp_changed_lines: {
    en: 'Changed lines:',
    ptb: 'Linhas alteradas:',
    de: 'Geänderte Zeilen:',
    fr: 'Lignes modifiées :',
    es: 'Líneas modificadas:',
    it: 'Righe cambiate:',
    ko: '변경된 줄:',
    jp: '変更された行：',
    ch: '更改的行：',
    cht: '已變更列：'
  },

  fp_copy_all: {
    en: 'Copy all',
    ptb: 'Copiar todas',
    de: 'Alle kopieren',
    fr: 'Copier toutes',
    es: 'Copiar todas',
    it: 'Copia tutte',
    ko: '모든 복사',
    jp: 'すべてコピー',
    ch: '全部复制',
    cht: '全部複製'
  }

};