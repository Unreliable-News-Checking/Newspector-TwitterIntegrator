import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';
// // Start writing Firebase Functions
// // https://firebase.google.com/docs/functions/typescript
//
// export const helloWorld = functions.https.onRequest((request, response) => {
//  response.send("Hello from Firebase!");
// });

"use strict";
admin.initializeApp();

interface Dic {
    [key: string]: Number
}


export const increaseFirstNewsScore = functions.firestore
    .document('clusters/{cluster_id}')
    .onCreate((snapshot, context) => {
        const data = snapshot.data();
        const db = admin.firestore();
        if (data) {
            const groupLeader = data.groupLeader;
            const accountRef = db.collection('accounts').doc(groupLeader);
            db.runTransaction(t => {
                return t.get(accountRef)
                    .then(doc => {
                        const accountData = doc.data();
                        if (accountData) {
                            const newNumber = accountData.number_of_first_news_in_group + 1;
                            t.update(accountRef, { number_of_first_news_in_group: newNumber });
                        }

                    }).catch(err => {
                        console.log('Update failure:', err);
                    });
            }).then(result => {
                console.log('Transaction success!');
            }).catch(err => {
                console.log('Transaction failure:', err);
            });
        }
    });

export const increaseNumberOfNews = functions.firestore
    .document('tweets/{tweet_id}')
    .onUpdate((change, context) => {
        const data = change.after.data();
        const db = admin.firestore();
        if (data) {
            const account = data.username;
            const accountRef = db.collection('accounts').doc(account);
            db.runTransaction(t => {
                return t.get(accountRef)
                    .then(doc => {
                        const accountData = doc.data();
                        if (accountData) {
                            const newNumber = accountData.number_of_total_news + 1;
                            t.update(accountRef, { number_of_total_news: newNumber });
                        }

                    }).catch(err => {
                        console.log('Update failure:', err);
                    });
            }).then(result => {
                console.log('Transaction success!');
            }).catch(err => {
                console.log('Transaction failure:', err);
            });
        }
    });

export const increaseNumberOfNewsInCategory = functions.firestore
    .document('tweets/{tweet_id}')
    .onUpdate((change, context) => {
        const data = change.after.data();
        const db = admin.firestore();
        if (data) {
            const account = data.username;
            let categoryOfTweet = data.category;
            const accountRef = db.collection('accounts').doc(account);
            db.runTransaction(t => {
                return t.get(accountRef)
                    .then(doc => {
                        const accountData = doc.data();
                        if (accountData) {
                            const categoryCount = accountData[categoryOfTweet];

                            if (categoryCount) {
                                const newData = <Dic>{
                                    [categoryOfTweet]: categoryCount + 1
                                };
                                t.update(accountRef, newData);
                            }
                            else {
                                const newData = <Dic>{
                                    [categoryOfTweet]: 1
                                };
                                t.set(accountRef, newData, { merge: true });
                            }

                        }
                    }).catch(err => {
                        console.log('Update failure:', err);
                    });
            }).then(result => {
                console.log('Transaction success!');
            }).catch(err => {
                console.log('Transaction failure:', err);
            });
        }
    });