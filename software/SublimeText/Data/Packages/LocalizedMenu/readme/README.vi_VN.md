# LocalizedMenu
Công cụ Viết bản địa hóa & Menu bản địa hóa cho Sublime Text 2/3/4

- Cung cấp cách dễ dàng để thêm ngôn ngữ mới
- Hỗ trợ nhiều phiên bản/nền tảng
- Hỗ trợ chia sẻ menu chung
- Tự động sao lưu menu cục bộ
- Tự động giải nén menu tiếng Anh của bản dựng mới

# README.md
- de_DE [Deutsch](readme/README.de_DE.md)
- en [English](README.md)
- es_ES [Español](readme/README.es_ES.md)
- fr_FR [Français](readme/README.fr_FR.md)
- hu [Magyar](readme/README.hu.md)
- hy [Հայերեն](readme/README.hy.md)
- pt_BR [Português do Brasil](readme/README.pt_BR.md)
- ru [Русский](readme/README.ru.md)
- sv_SE [Svenska](readme/README.sv_SE.md)
- vi_VN [Tiếng Việt](readme/README.vi_VN.md)
- zh_CN [简体中文](readme/README.zh_CN.md)
- zh_TW [繁体中文](readme/README.zh_TW.md)

# Dự án này cũng được lưu trữ tại
- [GitHub](https://github.com/zam1024t/LocalizedMenu)
- [Gitee](https://gitee.com/zam1024t/LocalizedMenu)

# Hình ảnh
#### Chạy trên Windows
![Work on Windows](https://raw.githubusercontent.com/zam1024t/LocalizedMenu/shots/shots/LocalizedMenu_win.gif)
#### Chạy trên OS X
![Work on OS X](https://raw.githubusercontent.com/zam1024t/LocalizedMenu/shots/shots/LocalizedMenu_osx.gif)
#### Chạy trên Ubuntu
![Work on Ubuntu](https://raw.githubusercontent.com/zam1024t/LocalizedMenu/shots/shots/LocalizedMenu_linux.gif)

# Cài đặt
- Bằng Package Control
	- cài đặt [Package Control](https://packagecontrol.io/installation)
	- tìm kiếm `LocalizedMenu`
- Thủ công
	- tải xuống [master.zip](https://github.com/zam1024t/LocalizedMenu/archive/master.zip), giải nén vào `Packages`, sau đó đổi tên `LocalizedMenu-master` thành `LocalizedMenu`
	- git clone vào `Packages`
	```
	git clone [https://github.com/zam1024t/LocalizedMenu](https://github.com/zam1024t/LocalizedMenu)
	```

# Cách sử dụng
- Chuyển đổi trong menu
	- thông qua `Tùy chọn` (`Preference`) -> `Ngôn ngữ` (`Languages`)
- Chuyển đổi trong bảng lệnh
	- `Ctrl+Shift+P`, nhập `lmxx` (*xx* là mã ngôn ngữ) để chuyển đổi

# Thêm một ngôn ngữ
- sao chép `locale/en/en.json` thành `locale/<locale>/<locale>.json`, dịch sang ngôn ngữ của bạn
- sao chép `menu/<version>/en/*` thành `menu/<version>/<locale>/*`, dịch sang ngôn ngữ của bạn
- Ví dụ, bây giờ thêm ngôn ngữ tên là `my` cho Sublime Text Build 3999
	- mở thư mục `LocalizedMenu`, thông qua `Tùy chọn` -> `Ngôn ngữ` -> `Thêm ngôn ngữ` (`Add a language`)
	- nhập `locale`, sao chép `en` thành `my`
	- nhập `my`, đổi tên `en.json` thành `my.json`, chỉnh sửa như sau:

	```JavaScript
	{
		"link": "",
		"hidden": false,
		"caption": "MyLanguage",
		"mnemonic": "m"
	}
	```

	- nhập `menu/3999`, sao chép `en` thành `my`, và dịch tất cả `caption` trong các tệp menu
	- nhận diện ngôn ngữ thông qua `Tùy chọn` -> `Ngôn ngữ` -> `Nhận diện` (`Detect`), sau đó `MyLanguage (my)` sẽ hiển thị

	> **Cấu hình ngôn ngữ**<br>
	> link: ngôn ngữ đích được liên kết tới<br>
	> hidden: ẩn mục menu<br>
	> caption: tên ngôn ngữ, mã ngôn ngữ sẽ được tự động thêm vào<br>
	> mnemonic: phím tắt, tùy chọn, đảm bảo caption có chứa nó, có phân biệt chữ hoa chữ thường

# Gửi đóng góp ngôn ngữ
- tên ngôn ngữ phải được đặt là `<languageCode>` hoặc `<languageCode>_<countryCode>`
	- `<languageCode>` chữ thường, `<countryCode>` chữ hoa (bỏ qua điều này nếu làm việc cục bộ)
	- Ngôn ngữ: https://www.wikipedia.org/wiki/ISO_639-1
	- Quốc gia: https://www.wikipedia.org/wiki/ISO_3166-1
- Fork kho lưu trữ
- Tạo pull request

# Ngôn ngữ & Người đóng góp
- de_DE Deutsch *by [Standarduser](https://github.com/Standarduser)*
- es Español *by [Christopher](https://t.me/Azriel_7589)*
- es_ES Español *by [Dastillero](https://github.com/dap39)*
- fr_FR Français *by [fxbenard](https://github.com/fxbenard)*
- hu Magyar *by [Tamás Balog](https://github.com/picimako)*
- hy Հայերեն *by [Arman High Foundation](https://github.com/ArmanHigh)*
- pt Português do Brasil *by [JNylson](https://github.com/jnylson)*
- ru Русский *by [Dimox](http://dimox.name) & [Ant0sh](https://github.com/Ant0sh) & [Maksim Arhipov](https://github.com/OSPanel)*
- sv_SE Svenska *by [H2SO4JB](https://github.com/H2SO4JB)*
- vi_VN Tiếng Việt *by [Vũ Anh Vũ](https://github.com/vuanhvu1982)*
- zh_CN 简体中文 *by [Zam](https://github.com/zam1024t)*
- zh_TW 繁体中文 *by [Zam](https://github.com/zam1024t)*

# Thảo luận liên quan
- https://github.com/wbond/package_control_channel/pull/5665
- https://github.com/rexdf/ChineseLocalization/issues/10

# Giấy phép
[Giấy phép MIT](LICENSE)