/*
	Real time subtitle translate for PotPlayer using LibreTranslate API
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
//------------------------------------------------------------------------------------------------
// array<string> GetSrcLangs() 												-> get source language
// array<string> GetDstLangs() 												-> get target language
// string Translate(string Text, string &in SrcLang, string &in DstLang) 	-> do translate !!

string JsonParseNew(string json)
{
	JsonReader Reader;
	JsonValue Root;
	string ret = "";	
	
	if (Reader.parse(json, Root) && Root.isObject())
	{
		JsonValue translatedText = Root["translatedText"];
		
		if (translatedText.isString())
		{
			ret = translatedText.asString();
		}
		else
		{
			JsonValue error = Root["error"];
		
			if (error.isString())
			{
				ret = error.asString();
			}
		}
	} 
	return ret;
}

array<string> LangTable = 
{
	"sq",
	"ar",
	"az",
	"bn",
	"bg",
	"ca",
	"cs",
	"da",
	"nl",
	"en",
	"eo",
	"et",
	"fi",
	"fr",
	"de",
	"el",
	"he",
	"hi",
	"hu",
	"id",
	"ga",
	"it",
	"ja",
	"ko",
	"lv",
	"lt",
	"ms",
	"nb",
	"fa",
	"pl",
	"pt",
	"pt-BR",
	"ro",
	"ru",
	"sr",
	"sk",
	"sl",
	"es",
	"sv",
	"tl",
	"th",
	"tr",
	"ur",
	"uk",
	"vi",
	"zh-Hant",
	"zh-Hans"
};

string UserAgent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36";

string GetTitle()
{
	return "{$CP949=Libre 번역$}{$CP950=Libre 翻譯$}{$CP0=Libre Translate$}";
}

string GetVersion()
{
	return "1";
}

string GetDesc()
{
	return "https://libretranslate.com/";
}

string GetLoginTitle()
{
	return "Input LibreTranslate API key or local http url";
}

string GetLoginDesc()
{
	return "Input LibreTranslate API key or local http url";
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
	array<string> ret = LangTable;
	
	ret.insertAt(0, ""); // empty is auto
	return ret;
}

array<string> GetDstLangs()
{
	array<string> ret = LangTable;
	
	return ret;
}

string Translate(string Text, string &in SrcLang, string &in DstLang)
{
//HostOpenConsole();	// for debug
	
//	by new API	
	if (api_key.length() > 0)
	{
		if (SrcLang.length() <= 0) SrcLang = "auto";
		SrcLang.MakeLower();
	
		string key = api_key;
		string enc = HostUrlEncode(Text);
		string url = "https://libretranslate.com/translate";
		string header = "accept: application/json\r\nContent-Type: application/x-www-form-urlencoded\r\n";	
		string post;
		if (key.find("http") == 0)
		{
			url = key;
			key = "";
		}
		post += "q=" + enc + "&";
		post += "source=" + SrcLang + "&";
		post += "target=" + DstLang + "&";
		post += "api_key=" + key + "&";
		post += "format=text";

		string text = HostUrlGetString(url, UserAgent, header, post);
		string ret = JsonParseNew(text);		
		if (ret.length() > 0)
		{
			SrcLang = "UTF8";
			DstLang = "UTF8";
			return ret;
		}	
	}
	
	return "";
}
