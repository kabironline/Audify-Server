-- Active: 1697795179051@@127.0.0.1@6379
SELECT Track.*
FROM "Track"
    INNER JOIN "Rating" ON Rating.track_id = Track.id
    INNER JOIN "Channel" ON Track.channel_id = Channel.id
WHERE
    Track.flagged IS NULL
    AND Channel.blacklisted IS NULL
GROUP BY Track.id
HAVING AVG(Rating.rating) > 0
ORDER BY AVG(Rating.rating) DESC