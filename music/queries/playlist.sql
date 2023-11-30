-- Active: 1697795179051@@127.0.0.1@6379
SELECT
    Track.*
FROM "Track"
    Inner join "PlaylistItem" ON Track.id = PlaylistItem.track_id
    Inner join "Channel" ON Track.channel_id = Channel.id
WHERE
    Channel.blacklisted is NULL
    AND Track.flagged is NULL
    AND PlaylistItem.playlist_id = 12
