import { makeAutoObservable, observable, runInAction } from 'mobx';
import { CreateCfaForm } from '../models/CreateCfaForm';
import { CfaApiServiceInstanse } from '../api/CfaApiService';
import { OffersApiServiceInstanse } from '../api/OffersApiService';
import { Offer } from '../api/models';
import { ProfileApiServiceInstanse } from '../api/ProfileApiService';
import { DesiresApiServiceInstanse } from '../api/DesiresApiService';
import { PredictionApiServiceInstanse } from '../api/PredictionApiService';
import { DealApiServiceInstanse } from '../api/DealApiService';
import { StatisticsApiServiceInstanse } from '../api/StatisticsApiService';

export class RootStore {
    public trigger: boolean = false;

    constructor() {
        makeAutoObservable(this, {
            trigger: observable,
        });
    }

    public setTrigger() {
        runInAction(() => {
            this.trigger = !this.trigger;
        });
    }

    public async createCfa(createCfaForm: CreateCfaForm): Promise<void> {
        const { id } = await CfaApiServiceInstanse.createCfa({
            count: createCfaForm.count,
            description: createCfaForm.description,
            title: createCfaForm.title,
        });

        if (createCfaForm.isInitialOfferActive && createCfaForm.price) {
            await OffersApiServiceInstanse.createOffer({
                cfa_image_id: id,
                count: createCfaForm.count,
                price: createCfaForm.price,
            });
        }
    }

    public async getCfaImages() {
        return await CfaApiServiceInstanse.getCfaImages();
    }

    public async getOffersByCfaImage(cfaImageId: number) {
        return await OffersApiServiceInstanse.getOffersByCfaImage(cfaImageId);
    }

    public async buyOffer(offer: Offer) {
        await OffersApiServiceInstanse.buyOffer(offer.id, {
            cfa_image_id: offer.cfa_image.id,
            count: offer.count,
            price: offer.price,
        });
    }

    public async deposit(amount: number) {
        await ProfileApiServiceInstanse.deposit({ value: amount });
    }

    public async withdraw(amount: number) {
        await ProfileApiServiceInstanse.withdraw({ value: amount });
    }

    public async getProfileInfo() {
        return await ProfileApiServiceInstanse.getProfileInfo();
    }

    public async getUserCfas(userId: number) {
        return await ProfileApiServiceInstanse.getUserCfas(userId);
    }

    public async createOffer(cfaImageId: number, count: number, price: number) {
        await OffersApiServiceInstanse.createOffer({ cfa_image_id: cfaImageId, count, price });
    }

    public async getOffersByUser(userId: number) {
        return await ProfileApiServiceInstanse.getOffersByUser(userId);
    }

    public async deleteOffer(offerId: number) {
        return await OffersApiServiceInstanse.deleteOffer(offerId);
    }

    public async createDesire(cfaImageId: number, count: number, price: number) {
        await DesiresApiServiceInstanse.createDesire({ cfa_image_id: cfaImageId, count, price });
    }

    public async deleteDesire(desireId: number) {
        return await DesiresApiServiceInstanse.deleteDesire(desireId);
    }

    public async getDesiresByCfaImage(cfaImageId: number) {
        return await DesiresApiServiceInstanse.getDesiresByCfaImage(cfaImageId);
    }

    public async sellDesire(desireId: number, count: number) {
        await DesiresApiServiceInstanse.sellDesire(desireId, {
            count,
        });
    }

    public async getDesiresByUser(userId: number) {
        return await ProfileApiServiceInstanse.getDesiresByUser(userId);
    }

    public async getCfaPricePrediction(cfaImageId: number): Promise<number[]> {
        return await PredictionApiServiceInstanse.fetchCfaPricePrediction(cfaImageId);
    }

    public async getIncomingDeals() {
        return await DealApiServiceInstanse.fetchIncomingDeals();
    }

    public async getOutgoingDeals() {
        return await DealApiServiceInstanse.fetchOutgoingDeals();
    }

    public async cancelDeal(dealId: number) {
        return await DealApiServiceInstanse.cancelDeal(dealId);
    }

    public async getCfaPriceHistory(cfaImageId: number) {
        return await CfaApiServiceInstanse.getCfaPriceHistory(cfaImageId);
    }

    public async getStatistics() {
        return await StatisticsApiServiceInstanse.fetchStatistics();
    }

    public async getUsersStatistics(sortBy: string = 'count') {
        return await StatisticsApiServiceInstanse.fetchUsersStatistics(sortBy);
    }

    public async getBuyAdvice(cfaImageId: number) {
        return await PredictionApiServiceInstanse.fetchBuyAdvice(cfaImageId);
    }
}
