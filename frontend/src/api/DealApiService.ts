import axios from 'axios';
import { API_URL } from '../config';
import authHeader from '../utils/authHeader';
import { Deal } from './models';

class DealApiService {
    public async fetchIncomingDeals() {
        console.log('incoming');

        const response = await axios.get<Deal[]>(`${API_URL}/user/deal/in`, {
            headers: authHeader(),
        });

        return response.data;
    }

    public async fetchOutgoingDeals() {
        const response = await axios.get<Deal[]>(`${API_URL}/user/deal/out`, {
            headers: authHeader(),
        });

        return response.data;
    }

    public async cancelDeal(dealId: number) {
        const response = await axios.post<void>(
            `${API_URL}/deal/cancel/${dealId}`,
            {},
            {
                headers: authHeader(),
            }
        );

        return response.data;
    }
}

export const DealApiServiceInstanse = new DealApiService();
