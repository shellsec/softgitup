/*
	real time subtitle translate for PotPlayer using bing API
	https://github.com/bmg0001/Bing-Translator-API
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
	"af",
	"sq",
	"am",
	"ar",
	"hy",
	"az",
	"eu",
	"be",
	"bn",
	"bh",
	"bs",
	"bg",
	"my",
	"ca",
	"ceb",
// 	"chr",
	"zh",
	"zh-CN",
	"zh-TW",
	"hr",
	"cs",
	"da",
// 	"dv",
	"nl",
	"en",
	"eo",
	"et",
	"tl",
	"fi",
	"fr",
	"gl",
	"ka",
	"de",
	"el",
// 	"gn",
	"gu",
	"ht",
	"ha",
	"iw",
	"hi",
	"hmn",
	"hu",
	"is",
	"ig",
	"id",
	"ga",
// 	"iu",
	"it",
	"ja",
	"jw",
	"kn",
	"kk",
	"km",
	"ko",
	"ku",
	"ky",
	"lo",
	"la",
	"lv",
	"lt",
	"mk",
	"ms",
	"ml",
	"mt",
	"mi",
	"mr",
	"mn",
	"ne",
	"no",
//	"or",
	"ps",
	"fa",
	"pl",
	"pt",
	"pa",
	"ro",
//	"romanji",
	"ru",
//	"sa",
	"sr",
	"sd",
	"st",
	"si",
	"sk",
	"sl",
	"so",
	"es",
	"sw",
	"sv",
	"sw",
	"tg",
	"ta",
//	"tl",
	"te",
	"th",
//	"bo",
	"tr",
	"uk",
	"ur",
	"uz",
//	"ug",
	"vi",
	"cy",
	"xh",
	"yi",
	"yo",
	"zu"
};

string UserAgent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari";

string GetTitle()
{
	return "{$CP949=Bing 번역$}{$CP950=微軟翻譯$}{$CP0=Bing translate$}";
}

string GetVersion()
{
	return "1";
}

string GetDesc()
{
	return "<a href=\"https://docs.microsoft.com/en-us/azure/cognitive-services/translator/translator-text-how-to-signup\">https://www.bing.com/translator/</a>";
}

string GetLoginTitle()
{
	return "Input microsoft API key";
}

string GetLoginDesc()
{
	return "Input microsoft API key";
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

array<string> GetSrcLangs()
{
	array<string> ret = LangTable;

	return ret;
}

array<string> GetDstLangs()
{
	array<string> ret = LangTable;
	
	return ret;
}

string Translate(string Text, string &in SrcLang, string &in DstLang)
{
	string UNICODE_RLE = "\u202B";
	
	if (SrcLang.length() <= 0) SrcLang = "en";
	
	string url = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from=" + SrcLang + "&to=" + DstLang;
	
	string SendHeader = "Ocp-Apim-Subscription-Key: " + api_key + "\r\n";
	// SendHeader += "Ocp-Apim-Subscription-Region:francecentral\r\n";
	SendHeader += "Content-Type: application/json\r\n";
	
	string Post = "[{\"Text\":\"" + Text + "\"}]";	
	
	string ret = "";
	uintptr http = HostOpenHTTP(url, UserAgent, SendHeader, Post);
	if (http != 0)
	{
		string json = HostGetContentHTTP(http);
		JsonReader Reader;
		JsonValue Root;
	
		if (Reader.parse(json, Root))
		{
			if (Root.isArray())
			{
				for (int i = 0, len = Root.size(); i < len; i++)
				{
					JsonValue child1 = Root[i];
					
					if (child1.isObject())
					{
						JsonValue translations = child1["translations"];

						if (translations.isArray())
						{
							for (int i = 0, len = translations.size(); i < len; i++)
							{
								JsonValue child2 = translations[i];						

								if (child2.isObject())
								{
									JsonValue text = child2["text"];
									
									if (!ret.empty()) ret = ret + "\n";
									if (text.isString()) ret = ret + text.asString();
								}
							}
						}
					}
				}
			}
			else if (Root.isObject())
			{
				JsonValue error = Root["error"];
				
				if (error.isObject())
				{
					JsonValue message = error["message"];
					
					if (message.isString()) ret = message.asString();
				}
			}
		}

		HostCloseHTTP(http);		
	}
	if (DstLang == "fa" || DstLang == "ar" || DstLang == "he") ret = UNICODE_RLE + ret;
	SrcLang = "UTF8";
	DstLang = "UTF8";
	
	
	return ret;
}
