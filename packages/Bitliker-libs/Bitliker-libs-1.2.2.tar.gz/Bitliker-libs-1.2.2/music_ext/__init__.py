#!/usr/bin/env python

"""
Author: Bitliker
Date: 2025-03-13 11:35:10
Version: 1.0
Description: 音乐 tag 维护处理
power by : [musictag](https://github.com/KristoforMaynard/music-tag)


"""
import os
import dataclasses
import music_tag


@dataclasses.dataclass
class MusicMeta:
    """Mp3 tag 信息模型"""
    title: str = ""  # 标题
    artist: list[str] = ""  # 艺术家
    composer: str = ""  # 作曲者
    album: str = ""  # 专辑
    album_artist: str = ""  # 专辑艺术家
    genre: list[str] = ""  # 流派
    year: int = 0  # 年份
    comment: str = ""  # 注释
    tracknumber: int = 0  # 音轨(章节)编号, 用来排序的, 1..totaltracks
    totaltracks: int = 0  # 音轨(章节)总数
    discnumber: int = 0  # 碟片(卷)编号, 用来排序的, 1..totaldiscs
    totaldiscs: int = 0  # 碟片(卷)总数
    # with open('path', 'rb') as in: in.read() 获取文件字节
    cover_image: bytes = ""  # 封面图片
    lyrics: str = ""  # 歌词
    language: str = "zh"


class MusicTag:
    """有声书维护"""

    def __init__(self):
        pass

    def read_tag(self, file_path: str) -> MusicMeta:
        """读取mp3 tag

        Args:
            file_path (str): 文件路径

        Returns:
            Mp3TagInfo: tag 信息
        """
        file_tag = music_tag.load_file(file_path)
        if isinstance(file_tag, music_tag.AudioFile):
            print(f"类型正确: {file_tag.tag_format}")
        print(file_tag)
        info = MusicMeta()
        # 标题
        if "tracktitle" in file_tag:
            info.title = file_tag["tracktitle"].first
        elif "title" in file_tag:
            info.title = file_tag["title"].first

        # 专辑
        if "album" in file_tag:
            info.album = file_tag["album"].first
        # 专辑艺术家
        if "albumartist" in file_tag:
            info.album_artist = file_tag["albumartist"].first
        # 艺术家
        if "artist" in file_tag:
            info.artist = file_tag["artist"].values
            if not info.album_artist:
                info.album_artist = file_tag["artist"].first
        # 作曲者
        if "composer" in file_tag:
            info.composer = file_tag["composer"].first
            if not info.album_artist:
                info.album_artist = file_tag["composer"].first
        # 流派
        if "genre" in file_tag:
            info.genre = file_tag["genre"].values
        # 年份
        if "year" in file_tag:
            info.year = file_tag["year"].first
        # 注释
        if "comment" in file_tag:
            info.comment = file_tag["comment"].first
        # 歌词
        if "lyrics" in file_tag:
            info.lyrics = file_tag["lyrics"].first
        # 封面
        if "artwork" in file_tag:
            info.cover_image = file_tag["artwork"].first.data
        # 音轨(章节)
        if "tracknumber" in file_tag:
            info.tracknumber = file_tag["tracknumber"].first
        if "totaltracks" in file_tag:
            info.totaltracks = file_tag["totaltracks"].first
        # 碟片(分卷)
        if "discnumber" in file_tag:
            info.discnumber = file_tag["discnumber"].first
        if "totaldiscs" in file_tag:
            info.totaldiscs = file_tag["totaldiscs"].first

        return info

    def write_tag(self, file_path: str, tag: MusicMeta) -> bool:
        """保存mp3 tag

        Args:
            file_path (str): mp3文件路径
            tag (Mp3TagInfo): tag内容

        Returns:
            bool: 是否成功
        """
        try:
            file_tag = music_tag.load_file(file_path)
            # 标题
            if tag.title:
                file_tag["tracktitle"] = tag.title.strip()
            # 艺术家
            if tag.artist:
                file_tag.remove_tag("artist")
                for a in tag.artist:
                    file_tag.append_tag("artist", a.strip())
            # 作曲者
            if tag.composer:
                file_tag["composer"] = tag.composer.strip()
            elif file_tag["artist"]:
                file_tag["composer"] = file_tag["artist"].first
            # 专辑艺术家
            if tag.album_artist:
                file_tag["albumartist"] = tag.album_artist
            elif file_tag["artist"]:
                file_tag["albumartist"] = file_tag["artist"].first
            # 专辑
            if tag.album:
                file_tag["album"] = tag.album.strip()
            # 流派
            if tag.genre:
                file_tag.remove_tag("genre")
                for g in tag.genre:
                    file_tag.append_tag("genre", g.strip())
            # 年份
            if tag.year:
                file_tag["year"] = tag.year
            # 注释
            if tag.comment:
                file_tag["comment"] = tag.comment.strip()
            # 音轨
            if tag.tracknumber:
                file_tag["tracknumber"] = tag.tracknumber
            if tag.totaltracks:
                file_tag["totaltracks"] = tag.totaltracks
            # 碟片
            if tag.discnumber:
                file_tag["discnumber"] = tag.discnumber
            if tag.totaldiscs:
                file_tag["totaldiscs"] = tag.totaldiscs
            if tag.lyrics:
                file_tag["lyrics"] = tag.lyrics
            if tag.cover_image:
                file_tag["artwork"] = tag.cover_image
            file_tag.save()
            print(f"写入mp3成功: {file_path}")
            return True
        except Exception as e:  # pylint: disable=broad-except
            print(f"写入mp3失败: {e}")
            return False

    def get_cover_image(self, file_path: str) -> bytes:
        """获取封面图片"""
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return None
        print(f"获取封面图片: {file_path}")
        with open(file_path, "rb") as img_in:
            return img_in.read()
        return None
