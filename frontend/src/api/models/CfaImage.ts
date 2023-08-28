import { User } from '../../models/User';

export interface CfaImage {
    id: number;
    title: string;
    user: User;
    description: string;
    count: number;
}
