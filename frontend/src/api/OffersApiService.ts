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
}

export const OffersApiServiceInstanse = new OffersApiService();
