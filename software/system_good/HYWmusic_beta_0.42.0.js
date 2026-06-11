/**
 * @name HYWmusic_beta
 * @version 0.42.0
 * @author Ryn
 * @description HYWmusic LX Music 音源脚本
 * @homepage https://github.com/Macrohard0001/HYWmusic_source
 * @license MIT
 *
 * 支持平台: 酷我音乐、酷狗音乐、QQ音乐、网易云音乐、咪咕音乐
 * 支持音质: 128k, 320k, flac
 * 生成时间: 2026-06-05
 */

'use strict'

const { EVENT_NAMES, request, on, send } = globalThis.lx

const API_BASE = 'http://103.79.184.141:3000'
const SUPPORTED_SOURCES = ["kw", "kg", "tx", "wy", "mg"]
const ALLOWED_QUALITIES = ["128k", "320k", "flac"]
const SCRIPT_VERSION = 'HYWmusic_beta_v0.42.0'

const PLATFORM_NAMES = {
  kw: '酷我音乐',
  kg: '酷狗音乐',
  tx: 'QQ音乐',
  wy: '网易云音乐',
  mg: '咪咕音乐'
}

const PLATFORM_QUALITIES = {
  kw: ["128k", "320k", "flac"],
  kg: ["128k", "320k", "flac"],
  tx: ["128k", "320k", "flac"],
  wy: ["128k", "320k", "flac"],
  mg: ["128k", "320k", "flac"]
}

const ERROR_MSG = {
  NETWORK: '网络请求失败',
  PARSE: '数据解析失败',
  NOT_FOUND: '资源不存在',
  NO_PERMISSION: '无访问权限',
  UNSUPPORTED: '不支持的平台',
  NO_SONG_ID: '歌曲ID不存在',
  GET_URL_FAILED: '获取音乐链接失败',
}

const httpRequest = (url) => new Promise((resolve, reject) => {
  const headers = {
    'X-Script-Version': SCRIPT_VERSION,
    'User-Agent': 'LX-Music/HYWmusic'
  }
  request(url, { headers }, (err, resp) => {
    if (err) return reject(new Error(ERROR_MSG.NETWORK))
    resolve(resp.body)
  })
})

const apiRequest = async (endpoint, params = {}) => {
  const query = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => k + '=' + encodeURIComponent(v))
    .join('&')
  const url = API_BASE + endpoint + (query ? '?' + query : '')

  const body = await httpRequest(url)
  let data
  try {
    data = typeof body === 'string' ? JSON.parse(body) : body
  } catch (e) {
    throw new Error(ERROR_MSG.PARSE)
  }

  if (data.code === 401 || data.code === 403) throw new Error(ERROR_MSG.NO_PERMISSION)
  if (data.code === 404) throw new Error(ERROR_MSG.NOT_FOUND)
  if (data.code !== 200) throw new Error(data.message || ERROR_MSG.NETWORK)
  return data
}

const getSongId = (source, musicInfo) => {
  switch (source) {
    case 'kg':
      return musicInfo.hash || musicInfo.songId || musicInfo.id || ''
    case 'tx':
      return musicInfo.songmid || musicInfo.strMediaMid || musicInfo.mid || musicInfo.id || ''
    case 'wy':
      return musicInfo.songId || musicInfo.songmid || musicInfo.id || ''
    case 'kw':
      return musicInfo.songId || musicInfo.rid || musicInfo.musicId || musicInfo.id || ''
    case 'mg':
      return musicInfo.copyrightId || musicInfo.songId || musicInfo.songmid || musicInfo.id || ''
    default:
      return musicInfo.songId || musicInfo.songmid || musicInfo.id || musicInfo.hash || ''
  }
}

const getPlatformQuality = (source, quality) => {
  const platformAllowed = PLATFORM_QUALITIES[source] || ALLOWED_QUALITIES
  return platformAllowed.includes(quality) ? quality : (platformAllowed[0] || '128k')
}

const getMusicUrl = async (source, musicInfo, quality) => {
  if (!SUPPORTED_SOURCES.includes(source)) {
    return Promise.reject(new Error(ERROR_MSG.UNSUPPORTED))
  }

  const songId = getSongId(source, musicInfo)
  if (!songId) {
    return Promise.reject(new Error(ERROR_MSG.NO_SONG_ID))
  }

  const finalQuality = getPlatformQuality(source, quality)
  const name = musicInfo.name || musicInfo.songName || musicInfo.title || ''
  const singer = musicInfo.singer || musicInfo.artist || musicInfo.artistName || ''

  const data = await apiRequest('/api/music/url', {
    source,
    songId,
    quality: finalQuality,
    name,
    singer
  })

  if (data.url) return data.url
  throw new Error(ERROR_MSG.GET_URL_FAILED)
}

const getLyric = async (source, musicInfo) => {
  const songId = getSongId(source, musicInfo)
  if (!songId) return { lyric: '', tlyric: '', rlyric: '', lxlyric: '' }

  try {
    const data = await apiRequest('/api/music/info', {
      action: 'lyric',
      source,
      songId
    })
    if (data.data) {
      return {
        lyric: data.data.lyric || '',
        tlyric: data.data.tlyric || '',
        rlyric: data.data.rlyric || '',
        lxlyric: data.data.lxlyric || ''
      }
    }
  } catch (e) {}
  return { lyric: '', tlyric: '', rlyric: '', lxlyric: '' }
}

const getPic = async (source, musicInfo) => {
  const songId = getSongId(source, musicInfo)
  if (!songId) return ''

  try {
    const data = await apiRequest('/api/music/info', {
      action: 'pic',
      source,
      songId
    })
    return data.data?.pic || ''
  } catch (e) {
    return ''
  }
}

on(EVENT_NAMES.request, ({ source, action, info }) => {
  switch (action) {
    case 'musicUrl':
      return getMusicUrl(source, info.musicInfo, info.type)
    case 'lyric':
      return getLyric(source, info.musicInfo)
    case 'pic':
      return getPic(source, info.musicInfo)
  }
})

send(EVENT_NAMES.inited, {
  sources: {
    kw: {
      name: '酷我音乐',
      type: 'music',
      actions: ['musicUrl', 'lyric', 'pic'],
      qualitys: ['128k', '320k', 'flac']
    },
    kg: {
      name: '酷狗音乐',
      type: 'music',
      actions: ['musicUrl', 'lyric', 'pic'],
      qualitys: ['128k', '320k', 'flac']
    },
    tx: {
      name: 'QQ音乐',
      type: 'music',
      actions: ['musicUrl', 'lyric', 'pic'],
      qualitys: ['128k', '320k', 'flac']
    },
    wy: {
      name: '网易云音乐',
      type: 'music',
      actions: ['musicUrl', 'lyric', 'pic'],
      qualitys: ['128k', '320k', 'flac']
    },
    mg: {
      name: '咪咕音乐',
      type: 'music',
      actions: ['musicUrl', 'lyric', 'pic'],
      qualitys: ['128k', '320k', 'flac']
    }
  }
})
