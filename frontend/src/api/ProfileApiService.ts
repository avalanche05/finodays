import axios from 'axios';
import { API_URL } from '../config';
import authHeader from '../utils/authHeader';
import { Balance, Desire, Offer } from './models';
import { IProfile } from './models/Profile';

class ProfileApiService {
    public async deposit(balance: Balance) {
        const response = await axios.post<void>(`${API_URL}/user/deposit`, balance, {
            headers: authHeader(),
        });

        return response.data;
    }

    public async withdraw(balance: Balance) {
        const response = await axios.post<void>(`${API_URL}/user/withdraw`, balance, {
            headers: authHeader(),
        });

        return response.data;
    }

    public async getProfileInfo(): Promise<IProfile> {
        const response = await axios.get<IProfile>(`${API_URL}/user/profile`, {
            headers: authHeader(),
        });

        return response.data;
    }

    public async getUserCfas(userId: number) {
        const response = await axios.get(`${API_URL}/user/cfa/${userId}`);

        return response.data;
    }

    public async getOffersByUser(userId: number): Promise<Offer[]> {
        const response = await axios.get<Offer[]>(`${API_URL}/user/offer/${userId}`, {
            headers: authHeader(),
        });

        return response.data;
    }

    public async getDesiresByUser(userId: number): Promise<Desire[]> {
        console.log(userId);

        const response = await axios.get<Desire[]>(`${API_URL}/user/desire/${userId}`, {
            headers: authHeader(),
        });

        return response.data;
    }
}

export const ProfileApiServiceInstanse = new ProfileApiService();
