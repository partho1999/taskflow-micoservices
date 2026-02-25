import { Router } from 'express'
import { uploadFile, getAll, getByTypeAndEntity } from '../controllers/attachment.controller.js'
import upload from '../middlewares/upload.middleware.js'

const router = Router()

router.post('/upload', upload.single('file'), uploadFile)
router.get('/', getAll)
router.get('/:entityType/:entityId', getByTypeAndEntity)

export default router