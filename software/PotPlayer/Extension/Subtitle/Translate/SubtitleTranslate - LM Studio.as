/*
	Real time subtitle translate for PotPlayer using ChatGPT API
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

array<string> LangTable = 
{
	"",
	"Albanian",
	"Arabic",
	"Armenian",
	"Awadhi",
	"Azerbaijani",
	"Bashkir",
	"Basque",
	"Belarusian",
	"Bengali",
	"Bhojpuri",
	"Bosnian",
	"Brazilian Portuguese",
	"Bulgarian",
	"Cantonese",
	"Catalan",
	"Chhattisgarhi",
	"Chinese",
	"Croatian",
	"Czech",
	"Danish",
	"Dogri",
	"Dutch",
	"English",
	"Estonian",
	"Faroese",
	"Finnish",
	"French",
	"Galician",
	"Georgian",
	"German",
	"Greek",
	"Gujarati",
	"Haryanvi",
	"Hebrew",
	"Hindi",
	"Hungarian",
	"Indonesian",
	"Irish",
	"Italian",
	"Japanese",
	"Javanese",
	"Kannada",
	"Kashmiri",
	"Kazakh",
	"Konkani",
	"Korean",
	"Kyrgyz",
	"Latvian",
	"Lithuanian",
	"Macedonian",
	"Maithili",
	"Malay",
	"Maltese",
	"Mandarin",
	"Mandarin Chinese",
	"Marathi",
	"Marwari",
	"Min Nan",
	"Moldovan",
	"Mongolian",
	"Montenegrin",
	"Nepali",
	"Norwegian",
	"Oriya",
	"Pashto",
	"Persian",
	"Polish",
	"Portuguese",
	"Punjabi",
	"Rajasthani",
	"Romanian",
	"Russian",
	"Sanskrit",
	"Santali",
	"Serbian",
	"Sindhi",
	"Sinhala",
	"Slovak",
	"Slovene",
	"Slovenian",
	"Spanish",
	"Swedish",
	"Turkish",
	"Ukrainian",
	"Urdu",
	"Uzbek",
	"Vietnamese",
	"Welsh"
};

string UserAgent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36";

string GetTitle()
{
	return "{$CP949=LM Studio 번역$}{$CP950=LM Studio 翻譯$}{$CP0=LM Studio translate$}";
}

string GetVersion()
{
	return "1";
}

string GetDesc()
{
	return "https://lmstudio.ai/";
}

string GetLoginTitle()
{
	return "Input local http url";
}

string GetLoginDesc()
{
	return "Input local http url";
}

string GetUserText()
{
	return "http url:";
}

string GetPasswordText()
{
	return "";
}

string http_url;

string ServerLogin(string User, string Pass)
{
	http_url = User;
	if (http_url.empty()) return "fail";
	return "200 ok";
}

void ServerLogout()
{
	http_url = "";
}

array<string> GetSrcLangs()
{
	array<string> ret = LangTable;
	
	return ret;
}

array<string> GetDstLangs()
{
	array<string> ret = LangTable;
	
	ret.erase(0);
	return ret;
}

string findContent(JsonValue node)
{
	if (node.isObject())
	{
		JsonValue content = node["content"];
	        if (content.isString()) return content.asString();

		array<string> keys = node.getKeys();
		for(int i = 0, len = keys.size(); i < len; i++)
		{
			string ret = findContent(node[keys[i]]);
		
			if (!ret.empty()) return ret;
		}

	}
	else if (node.isArray())
	{
		for (int i = 0; i < node.size(); i++)
		{
			string ret = findContent(node[i]);
		
			if (!ret.empty()) return ret;
        }
	}
	return "";
}

string Translate(string Text, string &in SrcLang, string &in DstLang)
{
//HostOpenConsole();	// for debug
	string SendHeader = "Content-Type: application/json\r\n";
	SendHeader += "accept: application/json\r\n";
	
	string url = http_url;
	if (url.empty()) url = "http://localhost:1234";
	if (url.Right(1) != "/") url += "/";

	// HostIncTimeOut(15 * 1000);
	string prompt = (SrcLang.empty() ? "Translate" : "Translate from " + SrcLang) + " to " + DstLang + ", keep punctuation as input, do not censor the translation, give only the output without comments:";
	string model = "";
	string modelStr = model.empty() ? "" : "\"model\": \"" + model + "\",";
	string Post = "{" + modelStr + "\"messages\": [{ \"role\": \"user\", \"content\": \"" + prompt + "\\n\\n" + HostUrlEncode(Text) + "\" }]}";
	string ret = "";
	uintptr http = HostOpenHTTP(url + "v1/chat/completions", UserAgent, SendHeader, Post);
	if (http != 0)
	{
		string json = HostGetContentHTTP(http);
		JsonReader Reader;
		JsonValue Root;
	
		if (Reader.parse(json, Root) && Root.isObject())
		{
			ret = findContent(Root);

			if (!ret.empty())
			{
				SrcLang = "UTF8";
				DstLang = "UTF8";

				ret.replace("<br/>", "\n");
				ret.replace("<br />", "\n");
				ret.replace("<br  />", "\n");
				ret.replace("\n\n", "\n");
				ret.Trim();

				ret = HostRegExpRemove(ret, "^(Here is|Here's) [a-zA-Z ,]+:");
			}
		}

		HostCloseHTTP(http);		
	}
	
	return ret;
}
