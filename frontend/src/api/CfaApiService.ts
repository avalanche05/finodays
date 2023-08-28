import axios from 'axios';
import { API_URL } from '../config';
import authHeader from '../utils/authHeader';
import { CfaImage, CreateCfaResponse } from './models';

class CfaApiService {
    public async createCfa(body: {
        count: number;
        description: string;
        title: string;
    }): Promise<CreateCfaResponse> {
        const response = await axios.post<CreateCfaResponse>(`${API_URL}/cfa-image/create`, body, {
            headers: authHeader(),
        });

        return response.data;
    }

    public async getCfaImages() {
        const response = await axios.get<CfaImage[]>(`${API_URL}/cfa-image/list`);

        return response.data;
    }
}

export const CfaApiServiceInstanse = new CfaApiService();
