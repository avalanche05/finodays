import { makeAutoObservable } from 'mobx';

export interface IRootStore {}

export class RootStore implements IRootStore {
    constructor() {
        makeAutoObservable(this, {});
    }
}
