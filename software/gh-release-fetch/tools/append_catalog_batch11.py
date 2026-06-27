#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""末批跨平台：Hashicorp/安全 CLI、VeraCrypt 等。"""
from __future__ import annotations

import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(ROOT, "apps")
BATCH = {}

def _add(p, s, apps): BATCH.setdefault((p,s),[]).extend(apps)
def _b(**kw):
    d = {"enabled":False,"prefer_api_assets":True,"version_tag_as_on_github":True,
         "windows_installer":False,"process_name":"","kill_before_install":False,"run_installer":False}
    d.update(kw); return d
def _repo(r): return {"releases_url":f"https://bgithub.xyz/{r}/releases","repo_path":r}
def _e(p,s,i,desc,cat,repo,**c):
    _add(p,s,[{"id":i,"简介":desc,"分类":cat,**_b(**c),**_repo(repo)}])
def _zip(i,s,cat,repo,desc,prefix,win_token="windows_amd64"):
    for p,tok,ex in (("linux","linux_amd64",["windows","darwin","386","arm"]),
                     ("darwin","darwin_amd64",["windows","linux","386","arm"])):
        _e(p,s,i,desc,cat,repo,installer_markers_match_all=True,installer_markers=[prefix,tok],
           href_exclude_substrings=ex,installer_extensions=[".zip"],
           download_names=[f"{prefix}{{ver}}_{tok}.zip"],save_name=f"{prefix}{{ver}}_{tok}.zip")

_zip("vault", "10-安全.json", "安全", "hashicorp/vault", "Vault", "vault_")
# trivy / terrascan 命名与 Hashicorp 不同，单独写
for p,m,ex in (("linux",["trivy_","Linux-64bit.zip"],["Windows","Darwin","macOS"]),
               ("darwin",["trivy_","macOS-64bit.zip"],["Windows","Linux","ARM"])):
    _e(p,"10-安全.json","trivy","Trivy（漏洞扫描）","安全","aquasecurity/trivy",
       installer_markers_match_all=True,installer_markers=m,href_exclude_substrings=ex,
       installer_extensions=[".zip"],use_download_filename=True,save_name=f"trivy-{p}.zip")
for p,m,ex in (("linux",["terrascan_","Linux_x86_64.zip"],["Windows","Darwin"]),
               ("darwin",["terrascan_","Darwin_x86_64.zip"],["Windows","Linux"])):
    _e(p,"10-安全.json","terrascan","Terrascan","安全","tenable/terrascan",
       installer_markers_match_all=True,installer_markers=m,href_exclude_substrings=ex,
       installer_extensions=[".zip"],use_download_filename=True,save_name=f"terrascan-{p}.zip")
for p,spec in (("linux",dict(installer_markers=["VeraCrypt_", "Setup-Linux-x64"],href_exclude_substrings=["win","mac","Portable"],
                             use_download_filename=True,save_name="VeraCrypt-Linux.run")),
               ("darwin",dict(installer_markers=["VeraCrypt_", "macOS.dmg"],href_exclude_substrings=["win","linux","Portable"],
                              installer_extensions=[".dmg"],use_download_filename=True,save_name="VeraCrypt.dmg"))):
    _e(p,"10-安全.json","veracrypt","VeraCrypt","安全","veracrypt/VeraCrypt",**spec)
for p,spec in (("linux",dict(installer_markers=["yubikey-manager-qt-", "linux.AppImage"],href_exclude_substrings=["win","mac"],
                             installer_extensions=[".AppImage"],use_download_filename=True,save_name="yubikey-manager.AppImage")),
               ("darwin",dict(installer_markers=["yubikey-manager-qt-", "mac.dmg"],href_exclude_substrings=["win","linux","AppImage"],
                              installer_extensions=[".dmg"],use_download_filename=True,save_name="yubikey-manager.dmg"))):
    _e(p,"10-安全.json","yubikey_manager","YubiKey Manager","安全","Yubico/yubikey-manager-qt",**spec)
_e("linux","10-安全.json","keepass","KeePass（Windows 专用；Linux 请用 keepassxc）","安全","KeePass/KeePass",
   prefer_api_assets=False,url_hint="keepass",releases_url="https://keepass.info/download.html",repo_path="KeePass/KeePass")
_e("darwin","10-安全.json","keepass","KeePass（macOS 无官方版；请用 keepassxc）","安全","KeePass/KeePass",
   prefer_api_assets=False,url_hint="keepass",releases_url="https://keepass.info/download.html",repo_path="KeePass/KeePass")

if __name__=="__main__":
    added=skipped=0
    for (plat,shard),apps in sorted(BATCH.items()):
        path=os.path.join(APPS,plat,shard)
        with open(path,encoding="utf-8") as f: data=json.load(f)
        seen={(a.get("id") or "").strip() for a in data if isinstance(a,dict)}
        for app in apps:
            aid=(app.get("id") or "").strip()
            if not aid or aid in seen: skipped+=1; continue
            data.append(app); seen.add(aid); added+=1
        with open(path,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=2); f.write("\n")
    print(f"written: added {added}, skipped {skipped}")
