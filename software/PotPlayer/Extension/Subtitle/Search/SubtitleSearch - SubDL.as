/*
	subtitle search by subDL
*/
 
// void OnInitialize()
// void OnFinalize()
// string GetTitle() 																-> get title for UI
// string GetVersion																-> get version for manage
// string GetDesc()																	-> get detail information
// string GetLoginTitle()															-> get title for login dialog
// string GetLoginDesc()															-> get desc for login dialog
// string GetUserText()																-> get user text for login dialog
// string GetPasswordText()															-> get password text for login dialog
// string ServerCheck(string User, string Pass) 									-> server check
// string ServerLogin(string User, string Pass) 									-> login
// void ServerLogout() 																-> logout
// string GetWebAccountUrl()							-> login process by WebBrowser
// string GetWebAccountDomain()							-> transport cookie domain for login
//------------------------------------------------------------------------------------------------
// string GetLanguages()															-> get support language
// string SubtitleWebSearch(string MovieFileName, dictionary MovieMetaData)			-> search subtitle bu web browser
// array<dictionary> SubtitleSearch(string MovieFileName, dictionary MovieMetaData)	-> search subtitle
// string SubtitleDownload(string id)												-> download subtitle
// string GetUploadFormat()															-> upload format
// string SubtitleUpload(string MovieFileName, dictionary MovieMetaData, string SubtitleName, string SubtitleContent)	-> upload subtitle

string UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29";

string GetTitle()
{
	return "SubDL";
}

string GetVersion()
{
	return "1";
}

string GetDesc()
{
	return "https://subdl.com/";
}

// https://subdl.com/api-files/language_list.json
array<array<string>> LangTable = 
{
    { "AR", "Arabic" },
    { "BR_PT", "Brazillian Portuguese" },
    { "DA", "Danish" },
    { "NL", "Dutch" },
    { "EN", "English" },
    { "FA", "Farsi_Persian" },
    { "FI", "Finnish" },
    { "FR", "French" },
    { "ID", "Indonesian" },
    { "IT", "Italian" },
    { "NO", "Norwegian" },
    { "RO", "Romanian" },
    { "ES", "Spanish" },
    { "SV", "Swedish" },
    { "VI", "Vietnamese" },
    { "SQ", "Albanian" },
    { "AZ", "Azerbaijani" },
    { "BE", "Belarusian" },
    { "BN", "Bengali" },
    { "ZH_BG", "Big 5 code" },
    { "BS", "Bosnian" },
    { "BG", "Bulgarian" },
    { "BG_EN", "Bulgarian_English" },
    { "MY", "Burmese" },
    { "CA", "Catalan" },
    { "ZH", "Chinese BG code" },
    { "HR", "Croatian" },
    { "CS", "Czech" },
    { "NL_EN", "Dutch_English" },
    { "EN_DE", "English_German" },
    { "EO", "Esperanto" },
    { "ET", "Estonian" },
    { "KA", "Georgian" },
    { "DE", "German" },
    { "EL", "Greek" },
    { "KL", "Greenlandic" },
    { "HE", "Hebrew" },
    { "HI", "Hindi" },
    { "HU", "Hungarian" },
    { "HU_EN", "Hungarian_English" },
    { "IS", "Icelandic" },
    { "JA", "Japanese" },
    { "KO", "Korean" },
    { "KU", "Kurdish" },
    { "LV", "Latvian" },
    { "LT", "Lithuanian" },
    { "MK", "Macedonian" },
    { "MS", "Malay" },
    { "ML", "Malayalam" },
    { "MNI", "Manipuri" },
    { "PL", "Polish" },
    { "PT", "Portuguese" },
    { "RU", "Russian" },
    { "SR", "Serbian" },
    { "SI", "Sinhala" },
    { "SK", "Slovak" },
    { "SL", "Slovenian" },
    { "TL", "Tagalog" },
    { "TA", "Tamil" },
    { "TE", "Telugu" },
    { "TH", "Thai" },
    { "TR", "Turkish" },
    { "UK", "Ukranian" },
    { "UR", "Urdu" }
};

string GetLanguages()
{
	string ret = "";
	
	for (int i = 0, len = LangTable.size(); i < len; i++)
	{
		if (ret.empty()) ret = LangTable[i][0];
		else ret = ret + "," + LangTable[i][0];
	}
	return ret;
}

string GetLoginTitle()
{
	return "Input API key";
}

string GetLoginDesc()
{
	return "Input API key";
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

string ServerCheck(string User, string Pass)
{
	return ServerLogin(User, Pass);
}

void ServerLogout()
{
	api_key = "";
}

void AssignItem(dictionary &dst, JsonValue &in src, string dst_key, string src_key = "")
{
	if (src_key.empty()) src_key = dst_key;
	if (src[src_key].isString()) dst[dst_key] = src[src_key].asString();
	else if (src[src_key].isInt64()) dst[dst_key] = src[src_key].asInt64();	
}

array<dictionary> SubtitleSearch(string MovieFileName, dictionary MovieMetaData)
{
//HostOpenConsole();	// for debug
	array<dictionary> ret;
    string url = "https://api.subdl.com/api/v1/subtitles?api_key=" + api_key + "&film_name=" + MovieFileName;
    string json = HostUrlGetString(url, UserAgent);
	JsonReader Reader;
	JsonValue Root;
	
	if (Reader.parse(json, Root) && Root.isObject())
	{
		JsonValue subtitles = Root["subtitles"];
		
		if (subtitles.isArray())
		{
			for (int j = 0, len = subtitles.size(); j < len; j++)
			{		
				JsonValue subtitle = subtitles[j];

                if (subtitle.isObject())
                {
					JsonValue url = subtitle["url"];
													
					if (url.isString())
					{													
						dictionary item;
                        JsonValue lang = subtitle["lang"];
                        JsonValue language = subtitle["language"];
                        JsonValue season = subtitle["season"];
                        JsonValue episode = subtitle["episode"];
							
                        item["format"] = "srt";
						item["id"] = url.asString();
                        AssignItem(item, subtitle, "fileName", "release_name");
                        if (lang.isString()) item["language"] = lang.asString();
                        if (language.isString()) item["lang"] = language.asString();
                        if (season.isInt()) item["seasonNumber"] = season.asInt();
                        if (episode.isInt()) item["episodeNumber"] = episode.asInt();
                        ret.insertLast(item);
                    }
                }
			}
        }
    }

	return ret;
}

string SubtitleDownload(string id)
{
	string api = "https://dl.subdl.com" + id;
	
	return HostUrlGetString(api);
}
