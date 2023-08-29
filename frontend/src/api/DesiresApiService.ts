import axios from 'axios';
import { API_URL } from '../config';
import authHeader from '../utils/authHeader';

class DesiresApiService {
    public async createDesire(body: { cfa_image_id: number; count: number; price: number }) {
        const response = await axios.post<void>(`${API_URL}/desire/create`, body, {
            headers: authHeader(),
        });

        return response.data;
    }

    public async getDesiresByCfaImage(cfaImageId: number) {
        const response = await axios.get(`${API_URL}/desire/list/${cfaImageId}`);

        return response.data;
    }

    public async sellDesire(desireId: number, body: { count: number }) {
        const response = await axios.post<void>(`${API_URL}/desire/sell/${desireId}`, body, {
            headers: authHeader(),
        });

        return response.data;
    }

    public async deleteDesire(desireId: number) {
        const response = await axios.post<void>(
            `${API_URL}/desire/cancel/${desireId}`,
            {},
            {
                headers: authHeader(),
            }
        );

        return response.data;
    }
}

export const DesiresApiServiceInstanse = new DesiresApiService();
