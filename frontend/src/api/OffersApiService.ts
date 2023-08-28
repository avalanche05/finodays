import axios from 'axios';
import { API_URL } from '../config';
import authHeader from '../utils/authHeader';

class OffersApiService {
    public async createOffer(body: { cfa_image_id: number; count: number; price: number }) {
        const response = await axios.post<void>(`${API_URL}/offer/create`, body, {
            headers: authHeader(),
        });

        return response.data;
    }

    public async getOffersByCfaImage(cfaImageId: number) {
        const response = await axios.get(`${API_URL}/offer/list/${cfaImageId}`);

        return response.data;
    }

    public async buyOffer(
        offerId: number,
        body: { cfa_image_id: number; count: number; price: number }
    ) {
        const response = await axios.post<void>(`${API_URL}/offer/buy/${offerId}`, body, {
            headers: authHeader(),
        });

        return response.data;
    }
}

export const OffersApiServiceInstanse = new OffersApiService();
