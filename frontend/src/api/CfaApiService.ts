import axios from 'axios';
import { API_URL } from '../config';
import authHeader from '../utils/authHeader';
import { CreateCfaResponse } from './models';

class CfaApiService {
    public async createCfa(body: { count: number; description: string; title: string }) {
        const response = await axios.post<CreateCfaResponse>(`${API_URL}/cfa-image/create`, body, {
            headers: authHeader(),
        });

        return response.data;
    }
}

export const CfaApiServiceInstanse = new CfaApiService();
