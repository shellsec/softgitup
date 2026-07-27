/*
	Real time subtitle translate for PotPlayer using DeepL API
*/

// void OnInitialize()
// void OnFinalize()
// string GetTitle() 														-> get title for UI
// string GetVersion														-> get version for manage
// string GetDesc()															-> get detail information
// string GetLoginTitle()													-> get title for login dialog
// string GetLoginDesc()													-> get desc for login dialog
// string GetUserText()														-> get user text for login dialog
// string GetPasswordText()													-> get password text for login dialog
// string ServerLogin(string User, string Pass)								-> login
// string ServerLogout()													-> logout
// string GetWebAccountUrl()							-> login process by WebBrowser
// string GetWebAccountDomain()							-> transport cookie domain for login
//------------------------------------------------------------------------------------------------
// array<string> GetSrcLangs() 												-> get source language
// array<string> GetDstLangs() 												-> get target language
// string Translate(string Text, string &in SrcLang, string &in DstLang) 	-> do translate !!

string JsonParse(string json)
{
	JsonReader Reader;
	JsonValue Root;
	string ret = "";	
	
	if (Reader.parse(json, Root) && Root.isObject())
	{
		JsonValue translations = Root["translations"];
		
		if (translations.isArray())
		{
			for (int i = 0, len = translations.size(); i < len; i++)
			{		
				JsonValue translation = translations[i];
				
				if (translation.isObject())
				{
					JsonValue text = translation["text"];
					
					if (text.isString())
					{				
						if (!ret.empty()) ret = ret + "\n";
						ret = ret + text.asString();
					}
				}
			}
		}
	} 
	return ret;
}

array<string> SrcLangTable = 
{
	"ar",
	"bg",
	"zh",
	"cs",
	"da",
	"nl",
	"en",
	"et",
	"fi",
	"fr",
	"de",
	"el",
	"hu",
	"id",
	"it",
	"ja",
	"ko",
	"lv",
	"lt",
	"nb",
	"pl",
	"pt",
	"ro",
	"ru",
	"sk",
	"sl",
	"es",
	"sv",
	"tr",
	"uk"
};

array<string> DstLangTable = 
{
	"ar",
	"bg",
	"zh",
	"cs",
	"da",
	"nl",
	"en-gb",
	"en-us",
	"et",
	"fi",
	"fr",
	"de",
	"el",
	"hu",
	"id",
	"it",
	"ja",
	"ko",
	"lv",
	"lt",
	"nb",
	"pl",
	"pt-pt",
	"pt-br",
	"ro",
	"ru",
	"sk",
	"sl",
	"es",
	"sv",
	"tr",
	"uk"
};

string UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36";

string GetTitle()
{
	return "{$CP949=DeepL 번역$}{$CP950=DeepL 翻譯$}{$CP0=DeepL translate$}";
}

string GetVersion()
{
	return "1";
}

string GetDesc()
{
	return "https://www.deepl.com";
}

string GetLoginTitle()
{
	return "Input DeepL auth key";
}

string GetLoginDesc()
{
	return "Input DeepL auth key";
}

string GetUserText()
{
	return "API key:";
}

string GetPasswordText()
{
	return "";
}

string api_key;
bool isFreeAPI = false;

string ServerLogin(string User, string Pass)
{
	api_key = User;
	if (api_key.empty()) return "fail";
	return "200 ok";
}

void ServerLogout()
{
	api_key = "";
}

array<string> GetSrcLangs()
{
	array<string> ret = SrcLangTable;
	
	ret.insertAt(0, ""); // empty is auto
	return ret;
}

array<string> GetDstLangs()
{
	array<string> ret = DstLangTable;
	
	return ret;
}

string Translate(string Text, string &in SrcLang, string &in DstLang)
{
//HostOpenConsole();	// for debug
	if (api_key.length() > 0)
	{
		SrcLang.MakeUpper();	
		string enc = HostUrlEncode(Text);
	
		string src;
		if (!SrcLang.empty()) src = "&source_lang=" + SrcLang;
		string url = "https://api.deepl.com/v2/translate?text=" + enc + src + "&target_lang=" + DstLang;
		string header = "Authorization: DeepL-Auth-Key " + api_key + "\r\n";
		string text;
		while (true)
		{
			if (isFreeAPI) url.replace("api.", "api-free.");
			text = HostUrlGetString(url, UserAgent, header);
			if (!isFreeAPI && text.find("api-free") > 0)
			{
				isFreeAPI = true;
				continue;
			}
			break;
		}
		string ret = JsonParse(text);
		if (ret.length() > 0)
		{
			string UNICODE_RLE = "\u202B";

			if (DstLang == "fa" || DstLang == "ar" || DstLang == "he") ret = UNICODE_RLE + ret;
			SrcLang = "UTF8";
			DstLang = "UTF8";
			return ret;
		}	
	}
	
	return "";
}
