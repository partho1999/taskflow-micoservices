import prisma from '../config/prisma.js'

export const createAttachment = async (data) => {
  return await prisma.attachment.create({ data })
}

export const getAllAttachments = async () => {
  return await prisma.attachment.findMany({
    orderBy: { createdAt: 'desc' }
  })
}

export const getByTypeAndEntity = async (type, entityId) => {
  return await prisma.attachment.findMany({
    where: { entityType: type, entityId }
  })
}