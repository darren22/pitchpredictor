# -*- coding: utf-8 -*-

pitchers = np.intersect1d( train_data.pitcher.unique(),test_data.pitcher.unique())
train_data = train_data[train_data.pitcher.isin(pitchers)]
test_data = test_data[test_data.pitcher.isin(pitchers)]


traine = SeasonEncoder(train_data,one_hot=False)
teste = SeasonEncoder(test_data,one_hot=False)
traine_data = traine.encoded_data
teste_data = teste.encoded_data

pitch_encodings = {val:idx for idx,val in 
                        enumerate(train_data.pitch_type
                    .unique())}
pitchsg_encodings = {val:idx for idx,val in 
                        enumerate(train_data.pitch_type_subgroup
                    .unique())}
pitchg_encodings = {val:idx for idx,val in 
                        enumerate(train_data.pitch_type_group
                    .unique())}

traine_labels = train_data.pitch_type.replace(pitch_encodings)
teste_labels = test_data.pitch_type.replace(pitch_encodings)

trainesg_labels = train_data.pitch_type_subgroup.replace(pitchsg_encodings)
testesg_labels = test_data.pitch_type_subgroup.replace(pitchsg_encodings)

traineg_labels = train_data.pitch_type_group.replace(pitchg_encodings)
testeg_labels = test_data.pitch_type_group.replace(pitchg_encodings)

rfc = RandomForestClassifier(n_estimators=100, max_depth=6)
rfc.fit(traine_data,traine_labels)
rfc.score(teste_data,teste_labels)

rfc = RandomForestClassifier(n_estimators=100, max_depth=6)
rfc.fit(traine_data,trainesg_labels)
rfc.score(teste_data,testesg_labels)

rfc = RandomForestClassifier(n_estimators=100, max_depth=6)
rfc.fit(traine_data,traineg_labels)
rfc.score(teste_data,testeg_labels)