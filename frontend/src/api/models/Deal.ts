import { CfaImage } from '.';
import { User } from '../../models/User';

export interface Deal {
    id: number;
    host: User;
    initiator: User;
    host_items: DealItem[];
    initiator_items: DealItem[];
}

export interface DealItem {
    cfa_image: CfaImage;
    count: number;
}
