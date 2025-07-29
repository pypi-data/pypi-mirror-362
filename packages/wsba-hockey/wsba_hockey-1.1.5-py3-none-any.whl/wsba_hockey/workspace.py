import numpy as np
import pandas as pd
import wsba_main as wsba
import data_pipelines as data
import numpy as np

season_load = wsba.repo_load_seasons()

select = season_load[0:3]

data.pbp(select)

#pbp = data.load_pbp_db(select)

#wsba.wsba_xG(pbp,hypertune=True,train=True,train_runs=30,cv_runs=30)
#select = season_load[3:18]
#for season in select:
#    wsba.nhl_apply_xG(data.load_pbp([season])).to_parquet(f'pbp/parquet/nhl_pbp_{season}.parquet',index=False)
#data.pbp_db(select)

#test = pd.read_parquet('aws_pbp/20242025.parquet')
#wsba.roc_auc_curve(test,'tools/xg_model/wsba_xg.joblib')
#wsba.feature_importance('tools/xg_model/wsba_xg.joblib')
#wsba.reliability(test,'tools/xg_model/wsba_xg.joblib')

#data.build_stats(['skater','team','goalie'],select)
#data.game_log(['skater','goalie'],select)
#data.fix_names(['skater','goalie'],select)

## DATA EXPORT ##
#data.push_to_sheet(select,['skaters','team','info'])