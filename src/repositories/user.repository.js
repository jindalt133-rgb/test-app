import { PrismaClient } from '@prisma/client';
export const prisma = new PrismaClient();
export const findUserByEmail = (email) => prisma.user.findUnique({ where: { email } });
export const createUser = ({ email, passwordHash }) => prisma.user.create({ data: { email, passwordHash } });
