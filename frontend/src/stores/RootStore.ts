import { makeAutoObservable } from 'mobx';
import { CreateCfaForm } from '../models/CreateCfaForm';
import { CfaApiServiceInstanse } from '../api/CfaApiService';
import { OffersApiServiceInstanse } from '../api/OffersApiService';
import { Offer } from '../api/models';

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
}
