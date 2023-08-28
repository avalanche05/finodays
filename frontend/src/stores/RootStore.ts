import { makeAutoObservable } from 'mobx';
import { CreateCfaForm } from '../models/CreateCfaForm';
import { CfaApiServiceInstanse } from '../api/CfaApiService';
import { OffersApiServiceInstanse } from '../api/OffersApiService';
import { Offer } from '../api/models';
import { ProfileApiServiceInstanse } from '../api/ProfileApiService';

export class RootStore {
    constructor() {
        makeAutoObservable(this, {});
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
}
