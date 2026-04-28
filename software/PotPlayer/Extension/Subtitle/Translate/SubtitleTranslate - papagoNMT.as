/*
	real time subtitle translate for PotPlayer using papago API
	https://developers.naver.com/docs/papago/
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

string UserAgent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari";

string GetTitle()
{
	return "{$CP949=네이버 파파고 번역(NMT)$}{$CP950=Naver papago 翻譯(NMT)$}{$CP0=Naver papago translate(NMT)$}";
}

string GetVersion()
{
	return "1";
}

string GetDesc()
{
	return "<a href=\"https://api.ncloud-docs.com/docs/ai-naver-papagonmt\">https://api.ncloud-docs.com/docs/ai-naver-papagonmt</a>";
}

string GetLoginTitle()
{
	return "Input Client ID/Secret";
}

string GetLoginDesc()
{
	return "Input Client ID/Secret";
}

string GetUserText()
{
	return "Client ID:";
}

string GetPasswordText()
{
	return "Client Secret:";
}

string client_id, client_secret;

string ServerLogin(string User, string Pass)
{
	client_id = User;
	client_secret = Pass;
	if (client_id.empty() || client_secret.empty()) return "fail";
	return "200 ok";
}

array<string> GetSrcLangs()
{
	array<string> ret;

	ret.insertLast("");
	ret.insertLast("en");
	ret.insertLast("ko");
	ret.insertLast("zh-CN");
	ret.insertLast("zh-TW");
	ret.insertLast("ja");
	return ret;
}

array<string> GetDstLangs()
{
	array<string> ret;
	
	ret.insertLast("ko");
	ret.insertLast("en");	
	ret.insertLast("zh-CN");
	ret.insertLast("zh-TW");
	ret.insertLast("ja");
	return ret;
}

string Translate(string Text, string &in SrcLang, string &in DstLang)
{		
	string SendHeader = "X-NCP-APIGW-API-KEY-ID: " + client_id + "\r\n";
	SendHeader += "X-NCP-APIGW-API-KEY: " + client_secret + "\r\n";
	SendHeader += "Content-Type: application/x-www-form-urlencoded; charset=UTF-8 \r\n";
	
	if (SrcLang.length() <= 0) SrcLang = "en";	
	
	string Post = "source=" + SrcLang + "&target=" + DstLang + "&text=" + HostUrlEncode(Text);
	string ret = "";
	uintptr http = HostOpenHTTP("https://naveropenapi.apigw.ntruss.com/nmt/v1/translation", UserAgent, SendHeader, Post);
	if (http != 0)
	{
		string json = HostGetContentHTTP(http);
		JsonReader Reader;
		JsonValue Root;
	
		if (Reader.parse(json, Root) && Root.isObject())
		{
			JsonValue message = Root["message"];
			
			if (message.isObject())
			{
				JsonValue result = message["result"];
				
				if (result.isObject())
				{
					JsonValue translatedText = result["translatedText"];
					
					if (translatedText.isString())
					{
						SrcLang = "UTF8";
						DstLang = "UTF8";
						ret = translatedText.asString();
					}
				}
			}
			else
			{
				JsonValue errorMessage = Root["errorMessage"];
				
				if (errorMessage.isString())
				{
					SrcLang = "UTF8";
					DstLang = "UTF8";
					ret = errorMessage.asString();
				}
			}
		}

		HostCloseHTTP(http);		
	}
	
	return ret;
}
