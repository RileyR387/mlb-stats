
db.tex.find({
},{
  'events.competitions.competitors': 1,
  'events.competitions.competitors.winner': 1,
  'events.competitions.competitors.record': 1,
  'events.competitions.competitors.team.shortDisplayName': 1,
  'events.competitions.competitors.score': 1,
}).sort({'stats_loader_timestamp':-1}).limit(1).pretty();

