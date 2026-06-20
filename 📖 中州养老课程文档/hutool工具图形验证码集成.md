---
tags: [中州养老, 项目]
date: 2026-06-06
---
-- CaptchaController -- 增加获取验证码接口（验证码类型支持更丰富）

	@GetMapping("/captchaImage")

	public AjaxResult getCode(HttpServletResponse response) throws IOException {

		// 1、判断验证码开关是否打开

		AjaxResult ajax = AjaxResult.success();

		boolean captchaEnabled = configService.selectCaptchaEnabled();

		ajax.put("captchaEnabled", captchaEnabled);

		if (!captchaEnabled) return ajax;



		// 2、声明验证码一系列变量

		String uuid = IdUtils.simpleUUID();

		String verifyKey = CacheConstants.CAPTCHA_CODE_KEY + uuid;

		String capStr,code = null;

		BufferedImage image = null;

		AbstractCaptcha captcha = null;



		// 3、各个渠道 - 生成验证码

		String captchaType = RuoYiConfig.getCaptchaType();

		switch (captchaType){

			case "math": // 谷歌数学四则运算

				String capText = captchaProducerMath.createText();

				capStr = capText.substring(0, capText.lastIndexOf("@"));

				code = capText.substring(capText.lastIndexOf("@") + 1);

				image = captchaProducerMath.createImage(capStr);

				break;

			case "char":  // 谷歌扭曲字符

				capStr = code = captchaProducer.createText();

				image = captchaProducer.createImage(capStr);

				break;

			case "hutool.line.char":{  // 线段干扰字符

				captcha = CaptchaUtil.createLineCaptcha(300, 100);

				break;

			}

			case "hutool.circle.char": { // 圆圈干扰字符

				captcha = CaptchaUtil.createCircleCaptcha(300, 100, 4, 20);

				break;

			}

			case "hutool.shear.char":{ // 扭曲干扰字符

				captcha = CaptchaUtil.createShearCaptcha(300, 100, 4, 4);

				break;

			}

			case "hutool.random.number":{  // 随机数字

				RandomGenerator randomGenerator = new RandomGenerator("0123456789", 4);

				//线段干扰字符样式

				captcha = CaptchaUtil.createLineCaptcha(300, 100);

				captcha.setGenerator(randomGenerator);

				captcha.createCode();

				break;

			}

			//该四则运算code中为 四则运算表达式本身，后续需借助MathGenerator对表达式进行验签

			case "hutool.math":{ // 四则运算

				captcha = CaptchaUtil.createShearCaptcha(300, 100, 4, 4);

				captcha.setGenerator(new MathGenerator());

				captcha.createCode();

				break;

			}

			case "hutool.gif":{  //动图

				captcha = CaptchaUtil.createGifCaptcha(300,100,4);

				/*captcha.setGenerator(new MathGenerator());

				captcha.createCode();*/

				break;

			}

			default:

				break;

		}



		// 4、转换流信息写出

		try {

			if(ObjectUtil.isNotEmpty(captcha)){

				code = captcha.getCode();

				byte[] imageBytes = captcha.getImageBytes();

				ajax.put("img", imageBytes);

			}else{

				// 转换流信息写出

				FastByteArrayOutputStream os = new FastByteArrayOutputStream();

				ImageIO.write(image, "jpg", os);

				String imageBytes = Base64.encode(os.toByteArray());

				ajax.put("img", imageBytes);

			}

		} catch (IOException e) {

			return AjaxResult.error(e.getMessage());

		}



		// 5、将验证码存入Redis，有效期 2 分钟

		redisCache.setCacheObject(verifyKey, code, Constants.CAPTCHA_EXPIRATION, TimeUnit.MINUTES);

		ajax.put("uuid", uuid);

		return ajax;

	}

	

-- application.yml -- 增加验证码配置

	# 验证码类型 math 数字计算 char 字符验证  hutool.line.char 线段干扰字符 hutool.circle.char 圆圈干扰字符 hutool.shear.char  扭曲干扰字符 hutool.random.number 随机数字  hutool.math 四则运算 hutool.gif 动图

	captchaType: hutool.gif

	

-- SysLoginService.validateCaptcha() -- 添加 hutool 四则运算校验逻辑

	# 验证码类型 math 数字计算 char 字符验证  hutool.line.char 线段干扰字符 hutool.circle.char 圆圈干扰字符 hutool.shear.char  扭曲干扰字符 hutool.random.number 随机数字  hutool.math 四则运算 hutool.gif 动图

	if(captcha.contains("=")){

		MathGenerator mathGenerator = new MathGenerator();

		if(!mathGenerator.verify(captcha, code)){

			AsyncManager.me().execute(AsyncFactory.recordLogininfor(username, Constants.LOGIN_FAIL, MessageUtils.message("user.jcaptcha.error")));

			throw new CaptchaException();

		}

	}else if (!code.equalsIgnoreCase(captcha))

	{

		AsyncManager.me().execute(AsyncFactory.recordLogininfor(username, Constants.LOGIN_FAIL, MessageUtils.message("user.jcaptcha.error")));

		throw new CaptchaException();

	}

## 相关笔记

- [[📖 中州养老课程文档/中州养老课程总览|中州养老课程总览]]
