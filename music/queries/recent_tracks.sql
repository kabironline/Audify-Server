-- Active: 1697795179051@@127.0.0.1@6379

SELECT
    Track.*,
    Channel.name as channel_name
FROM "Track"
    Inner join "Recent" ON Track.id = Recent.track_id
    Inner join "Channel" ON Track.channel_id = Channel.id
WHERE
    Recent.user_id = 19
    AND Channel.blacklisted is NULL
    AND Track.flagged is NULL
ORDER BY
    Recent.last_modified_at DESC